# main.py - Sony E-mount lens driver for the Chronos 1.4 lens control board
# RP2040 / MicroPython (tested against MicroPython 1.20+ APIs)
#
# The board acts as the camera BODY on the E-mount bus:
#   * powers the lens when LENS_DET (GP4) goes low
#   * runs the A6000-style init handshake (0x01 07 0C 0B 08 09 0D 10 0A)
#   * runs the 60 Hz normal loop: lens sends 0x05 + 0x06, we answer 0x03 + 0x04
#   * holds the lens in manual-focus-by-wire ("focus follow", 0x04 pl[3] = 0x81)
#     so the lens's own focus ring drives focus
#   * GP8/GP9 step the aperture, GP12/GP13 drive focus with a smooth ramp,
#     GP14 toggles OSS (see OSS_FIELD below), GP15 ejects the lens:
#     graceful shutdown (0x0A all-zero + 0x16), then power off
#   * SSD1306 128x64 on I2C1 (SDA GP10, SCL GP11) shows live status
#   * LENS_DET going high cuts lens power at once, from a hard IRQ
#
# Protocol facts come from the E-mount-protocol-RE notes; fields marked
# UNKNOWN there are filled with values copied from real body captures.

import time
import gc
import framebuf
import micropython
from machine import Pin, UART, I2C, PWM, mem32
from micropython import const

# --------------------------------------------------------------------------
# Pin map (control_board.sch)
# --------------------------------------------------------------------------
PIN_TXD = const(0)      # B_TO_L_TXD   J2-8   UART0 TX
PIN_RXD = const(1)      # L_TO_B_RXD   J2-7   UART0 RX
PIN_LCS = const(2)      # L_CS_B       J2-6   lens->body CS (input, unused)
PIN_BCS = const(3)      # B_CS_L       J2-9   body->lens CS (output)
PIN_DET = const(4)      # LENS_DET     J2-10  10k pull-up (R9); low = lens on
PIN_VD = const(5)       # BODY_VD_LENS J2-4   60 Hz frame sync
PIN_LOGIC = const(6)    # Q2 gate, 10k pull-up: low = LOGIC_VCC on
PIN_PWR = const(7)      # Q3 gate: output low = LENS_PWR on, input = off
PIN_SDA = const(10)     # OLED (I2C1)
PIN_SCL = const(11)

BTN_AP_OPEN = 8         # aperture: open (smaller f-number)
BTN_AP_CLOSE = 9        # aperture: close (larger f-number)
BTN_FOCUS_DOWN = 12     # focus toward the LOWER travel limit
BTN_FOCUS_UP = 13       # focus toward the UPPER travel limit
BTN_OSS_TOGGLE = 14     # OSS on/off toggle
BTN_EJECT = 15          # eject: stop comms cleanly, then cut lens power

# --------------------------------------------------------------------------
# Tunables
# --------------------------------------------------------------------------
DET_DEBOUNCE_MS = 150       # lens must read present this long before power-up
LENS_BOOT_MS = 0            # the handshake itself waits for the lens to boot
BAUD_INIT = 750000
BAUD_SPEED = (750000, 1500000, 3000000)  # speeds 0/1/2 (0x07 pl[1] bits 1/2)
MAX_SPEED = 1               # 2 = allow 3 Mbaud; no lens is known to declare it
PIN_HS_TIMEOUT_MS = 2000    # bodies give the lens ~2 s per pin-handshake step
PIN_HS_STRICT = False       # True: a missed CS step aborts, like a body does
# Pin-handshake trace: at power-up, step the body lines one at a time with a
# pause after each and log every change on RXD / L_CS_B (timestamped, printed
# when done). Also traces the speed-change handshake. Adds ~3 s to power-up.
PIN_HS_TRACE = False
TRACE_STEP_MS = (300, 500, 500, 800, 800)   # pause after each power-up step
POWEROFF_RXD_LOW_MS = 3000  # after 0x16, wait this long for the lens to drop RXD
VD_FREQ = 60
VD_LOW_US = 400             # width of the low-going VD pulse (not documented)
CS_LEAD_US = 20
CS_TRAIL_US = 5
INIT_TIMEOUT_MS = 200
INIT_0x10_TIMEOUT_MS = 10000  # 0x10 reply takes ~1.3 s; bodies wait forever
LOOP_TIMEOUT_MS = 400       # no 0x06 for this long = link lost
SHUTDOWN_ACK_MS = 2500      # the lens acks 0x16 only once it has parked:
                            # ~550 ms on a SEL2870, ~15 ms on a manual lens

APERTURE_REPEAT_DELAY_MS = 400
APERTURE_REPEAT_MS = 150

FOCUS_FULL_TRAVEL_S = 1.5   # full travel time at top speed
FOCUS_RAMP_S = 1.0          # time to ramp from crawl to top speed
FOCUS_CRAWL_FRACTION = 1 / 3000  # starting speed, fraction of travel per frame

# Lens name (message 0x3F). The A6000 never asks for it and Sony natives do
# not implement it; set True to try it on third-party lenses that advertise it.
REQUEST_LENS_NAME = False

# OSS: the protocol notes do not document an OSS command. GP14 toggles
# S.oss_req; if you find the bit, put (payload index in 0x03, off, on) here.
# (NEX-7 captures rule out 0x03 pl[12]/pl[13]/pl[15]: they toggle the same
# way for manual primes, so they are frame-timing fields, not OSS.)
OSS_FIELD = None

I2C_FREQ = 1000000          # drop to 400000 if the OLED misbehaves
OLED_ADDR = 0x3C

DEBUG = True

# 0x05 row index the body requests in 0x03 pl[21..22]; the lens echoes it two
# cycles later. Pattern an A6000 plays to a SELP1650: 15 16 x3, then 15 17 x3.
ROW_PATTERN = ((0x15, 0x16),) * 3 + ((0x15, 0x17),) * 3

# --------------------------------------------------------------------------
# Low-level helpers
# --------------------------------------------------------------------------
_GPIO_IN = const(0xD0000004)
_PADS_GP1 = const(0x4001C008)   # PADS_BANK0 GPIO1: bit 3 PUE, bit 2 PDE
_GPIO_OUT_SET = const(0xD0000014)
_GPIO_OE_SET = const(0xD0000024)
_GPIO_OE_CLR = const(0xD0000028)
_CTRL_GP0 = const(0x40014004)   # IO_BANK0 GPIO0_CTRL
_CTRL_GP3 = const(0x4001401C)
_CTRL_GP5 = const(0x4001402C)
_FUNC_SIO = const(5)
_BIT_PWR = const(0x80)          # GP7
_BIT_LOGIC = const(0x40)        # GP6
_BITS_SIG = const(0x29)         # GP0 | GP3 | GP5


def log(*a):
    if DEBUG:
        print(*a)


@micropython.native
def _csum(buf, start, end):
    s = 0
    for i in range(start, end):
        s += buf[i]
    return s & 0xFFFF


def _u16(b, o):
    return b[o] | (b[o + 1] << 8)


def _bcd(b):
    return (b >> 4) * 10 + (b & 0x0F)


def av_to_fnum(v):
    # aperture value = 256 * AV + 4096, N = 2^(AV/2)
    return 2 ** ((v - 4096) / 512)


def dist_code_to_m(c):
    # distance code = 384 + 64 * log2(metres); 0x0700 = infinity / not reported
    return 2 ** ((c - 384) / 64)


class LensGone(Exception):
    pass


class LinkError(Exception):
    pass


class EjectRequest(Exception):
    pass


# --------------------------------------------------------------------------
# Shared state (written by the session, read by the UI)
# --------------------------------------------------------------------------
class State:
    def __init__(self):
        self.reset()
        self.oss_req = False

    def reset(self):
        self.phase = "nolens"   # nolens / power / init / run / error
        self.msg = ""
        self.native = True
        self.lens_id = 0
        self.name = ""
        self.ap_max = 0         # widest aperture (0x08 pl[0..1])
        self.ap_min = 0         # narrowest aperture (0x08 pl[2..3])
        self.fl_short = 0       # mm, from 0x08 BCD
        self.fl_long = 0        # mm, 0 on a prime
        self.ap = 0             # current aperture (0x05 pl[0..1])
        self.ap_cmd = 0         # commanded aperture (0x03 pl[5..6]), 0 = follow lens
        self.dist = 0x0700      # 0x05 pl[20..21]
        self.flags05 = 0        # 0x05 pl[22]
        self.focal = 0          # 0x05 pl[24..25], mm x 10
        self.ring = 0           # 0x05 pl[60]
        self.switch = 0         # 0x05 pl[62]
        self.row_lo = 0         # 0x05 pl[77]
        self.row_hi = 0         # 0x05 pl[78]
        self.st06 = 0           # 0x06 pl[0]
        self.dir06 = 0          # 0x06 pl[1]
        self.pos = 0            # 0x06 pl[20..21]
        self.lim_lo = 0         # 0x06 pl[7..8]
        self.lim_hi = 0         # 0x06 pl[9..10]
        self.seq = 0
        self.frames = 0
        self.bad = 0
        self.focus_mode = "MF"  # MF / DRIVE / STOP


S = State()

# --------------------------------------------------------------------------
# Lens power and the detach interrupt
# --------------------------------------------------------------------------
det = Pin(PIN_DET, Pin.IN)              # external 10k pull-up
pwr = Pin(PIN_PWR, Pin.IN)              # input = lens power off
logic = Pin(PIN_LOGIC, Pin.OUT, value=1)  # high = lens logic off
_removed = False


def _det_irq(pin):
    # Hard IRQ: register writes only, no heap allocation.
    global _removed
    mem32[_GPIO_OE_CLR] = _BIT_PWR      # GP7 -> input: LENS_PWR off
    mem32[_GPIO_OUT_SET] = _BIT_LOGIC   # GP6 high: LOGIC_VCC off
    mem32[_GPIO_OE_SET] = _BIT_LOGIC
    # Tri-state TXD, B_CS_L and VD so an unpowered lens is not back-fed.
    mem32[_GPIO_OE_CLR] = _BITS_SIG
    mem32[_CTRL_GP0] = _FUNC_SIO
    mem32[_CTRL_GP3] = _FUNC_SIO
    mem32[_CTRL_GP5] = _FUNC_SIO
    _removed = True


det.irq(trigger=Pin.IRQ_RISING, handler=_det_irq, hard=True)


def lens_present():
    return det.value() == 0


def lens_power_on():
    global _removed
    _removed = False
    pwr.init(Pin.OUT, value=0)      # drive low -> Q3 on -> LENS_PWR
    logic.init(Pin.OUT, value=0)    # drive low -> Q2 on -> LOGIC_VCC


def lens_power_off():
    pwr.init(Pin.IN)
    logic.init(Pin.OUT, value=1)
    for n in (PIN_TXD, PIN_BCS, PIN_VD):
        Pin(n, Pin.IN)


# --------------------------------------------------------------------------
# SSD1306, pushed one 128-byte page at a time so it never blocks the lens loop
# --------------------------------------------------------------------------
class OLED(framebuf.FrameBuffer):
    W = 128
    H = 64

    def __init__(self, i2c, addr=OLED_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(self.W * self.H // 8)
        self.mv = memoryview(self.buf)
        super().__init__(self.buf, self.W, self.H, framebuf.MONO_VLSB)
        self._c = bytearray(2)
        for cmd in (0xAE, 0x20, 0x00, 0x40, 0xA1, 0xA8, 0x3F, 0xC8, 0xD3, 0x00,
                    0xDA, 0x12, 0xD5, 0x80, 0xD9, 0xF1, 0xDB, 0x30, 0x81, 0xCF,
                    0xA4, 0xA6, 0x8D, 0x14, 0xAF):
            self.cmd(cmd)
        self.fill(0)
        for p in range(8):
            self.push_page(p)

    def cmd(self, c):
        self._c[0] = 0x80
        self._c[1] = c
        self.i2c.writeto(self.addr, self._c)

    def push_page(self, p):
        for c in (0x21, 0, 127, 0x22, p, p):
            self.cmd(c)
        self.i2c.writevto(self.addr, (b"\x40", self.mv[p * 128:(p + 1) * 128]))


# --------------------------------------------------------------------------
# Buttons (active low, external 10k pull-ups)
# --------------------------------------------------------------------------
class Button:
    DEBOUNCE_MS = 20

    def __init__(self, n):
        self.pin = Pin(n, Pin.IN)
        self.raw = False
        self.down = False
        self.t_change = 0
        self.t_down = 0
        self.t_rep = 0
        self.pressed = False    # edge, cleared by the reader

    def update(self, now):
        r = self.pin.value() == 0
        if r != self.raw:
            self.raw = r
            self.t_change = now
        elif r != self.down and time.ticks_diff(now, self.t_change) >= self.DEBOUNCE_MS:
            self.down = r
            if r:
                self.pressed = True
                self.t_down = now
                self.t_rep = now

    def take_press(self):
        p = self.pressed
        self.pressed = False
        return p

    def repeat(self, now):
        # True on the press, then every APERTURE_REPEAT_MS after the delay
        if self.take_press():
            return True
        if self.down and time.ticks_diff(now, self.t_down) >= APERTURE_REPEAT_DELAY_MS \
                and time.ticks_diff(now, self.t_rep) >= APERTURE_REPEAT_MS:
            self.t_rep = now
            return True
        return False


# --------------------------------------------------------------------------
# UI: buttons + display
# --------------------------------------------------------------------------
class UI:
    def __init__(self):
        self.btn_open = Button(BTN_AP_OPEN)
        self.btn_close = Button(BTN_AP_CLOSE)
        self.btn_fdown = Button(BTN_FOCUS_DOWN)
        self.btn_fup = Button(BTN_FOCUS_UP)
        self.btn_oss = Button(BTN_OSS_TOGGLE)
        self.btn_eject = Button(BTN_EJECT)
        self.buttons = (self.btn_open, self.btn_close, self.btn_fdown,
                        self.btn_fup, self.btn_oss, self.btn_eject)
        self.eject_req = False  # set by GP15, consumed by the session/main
        self.oled = None
        try:
            i2c = I2C(1, sda=Pin(PIN_SDA), scl=Pin(PIN_SCL), freq=I2C_FREQ)
            self.oled = OLED(i2c)
        except OSError as e:
            log("OLED not found:", e)
        self.page = 8           # 8 = render a new frame before pushing page 0
        self.t_page = 0
        self.budget = 0         # pages allowed in the current quiet window
        self.focus_dir = 0      # -1 / 0 / +1, read by the session

    # ---- input -----------------------------------------------------------
    def poll_buttons(self):
        now = time.ticks_ms()
        for b in self.buttons:
            b.update(now)
        d = 0
        if self.btn_fdown.down:
            d -= 1
        if self.btn_fup.down:
            d += 1
        self.focus_dir = d
        if self.btn_oss.take_press():
            S.oss_req = not S.oss_req
        if self.btn_eject.take_press():
            self.eject_req = True
        step = 0
        if self.btn_open.repeat(now):
            step -= 1
        if self.btn_close.repeat(now):
            step += 1
        if step and S.phase == "run":
            self.step_aperture(step)

    def step_aperture(self, step):
        base = S.ap_cmd or S.ap
        if not base:
            return
        thirds = round((base - 4096) * 3 / 256) + step
        v = 4096 + (thirds * 256) // 3
        lo = S.ap_max if 4096 <= S.ap_max < 8000 else 4096
        hi = S.ap_min if S.ap_min > lo else 0x1900   # f/22 fallback
        S.ap_cmd = max(lo, min(hi, v))

    # ---- output ----------------------------------------------------------
    def service(self, free_run):
        """Poll buttons; push at most one display page.
        free_run: True when no lens loop is running (pace by time instead
        of by the quiet window after each 0x04)."""
        self.poll_buttons()
        if not self.oled:
            return
        now = time.ticks_ms()
        if free_run:
            if time.ticks_diff(now, self.t_page) < 4:
                return
        elif self.budget <= 0:
            return
        else:
            self.budget -= 1
        self.t_page = now
        if self.page >= 8:
            self.render()
            self.page = 0
            gc.collect()
            return
        self.oled.push_page(self.page)
        self.page += 1

    def render(self):
        o = self.oled
        o.fill(0)
        ph = S.phase
        if ph == "nolens":
            o.text("No lens", 36, 20)
            o.text("attached", 32, 34)
            return
        if ph == "ejected":
            o.text("Lens ejected", 16, 12)
            o.text("Safe to remove", 8, 30)
            o.text("EJECT=reconnect", 4, 48)
            return
        if ph in ("power", "init", "error", "eject"):
            o.text({"power": "Lens detected", "init": "Initialising",
                    "error": "Lens error", "eject": "Ejecting..."}[ph], 0, 16)
            o.text(S.msg[:16], 0, 32)
            o.text(S.msg[16:32], 0, 42)
            return
        # ---- running ----
        o.text((S.name or "ID 0x%04X" % S.lens_id)[:16], 0, 0)
        cur = "f/%.1f" % av_to_fnum(S.ap) if S.ap else "f/--"
        if S.ap_cmd and abs(S.ap_cmd - S.ap) > 40:
            cur += ">%.1f" % av_to_fnum(S.ap_cmd)
        o.text(cur, 0, 9)
        arrow = {0x02: ">", 0x04: "<"}.get(S.dir06, " ")
        o.text("Foc %5d%s%s" % (S.pos, arrow, "R" if S.ring else ""), 0, 18)
        # focus bar
        o.rect(0, 27, 128, 6, 1)
        span = S.lim_hi - S.lim_lo
        if span > 0:
            x = (S.pos - S.lim_lo) * 124 // span
            x = max(0, min(124, x))
            o.fill_rect(2, 29, x, 2, 1)
        if S.dist == 0 or S.dist >= 0x0700:
            o.text("Dist  --", 0, 35)
        else:
            o.text("Dist %.2fm" % dist_code_to_m(S.dist), 0, 35)
        if S.fl_long:
            o.text("Zoom %dmm" % ((S.focal + 5) // 10), 0, 44)
        else:
            o.text("%dmm prime" % ((S.focal + 5) // 10 or S.fl_short), 0, 44)
        oss = "ON " if S.oss_req else "OFF"
        o.text("OSS:%s%s" % (oss, " ?" if OSS_FIELD is None else ""), 0, 53)
        o.text(S.focus_mode, 104, 53)

    def quiet_window(self, pages=2):
        self.budget = pages


# --------------------------------------------------------------------------
# The bus session (one lens power-up)
# --------------------------------------------------------------------------
MAX_FRAME = const(512)


class Session:
    def __init__(self, ui):
        self.ui = ui
        self.rx = bytearray(2048)
        self.rxmv = memoryview(self.rx)
        self.fill = 0
        self.tx = bytearray(80)
        self.txmv = memoryview(self.tx)
        self.reply = None
        self.pending_seq = -1
        self.t_last06 = 0
        self.first03 = True
        self.cycle = 0
        self.row_i = 0
        self.trace = None
        self.body0 = 0x2EBB
        self.lens_bitmap = 0
        # focus drive state
        self.f_state = 0        # 0 idle (MF follow), 1 driving, 2 stopping
        self.f_target = 0.0
        self.f_v = 0.0
        self.f_stop_frames = 0
        self.uart = None
        self.vd = None
        self.bcs = None

    # ---- hardware --------------------------------------------------------
    def start_bus(self):
        self.bcs = Pin(PIN_BCS, Pin.OUT, value=0)
        self.lcs = Pin(PIN_LCS, Pin.IN)
        self.vd = PWM(Pin(PIN_VD))
        self.vd.freq(VD_FREQ)
        period_us = 1000000 // VD_FREQ
        self.vd.duty_u16(65535 - (65535 * VD_LOW_US) // period_us)
        self.set_baud(BAUD_INIT)

    @staticmethod
    def _rxd_high():
        return (mem32[_GPIO_IN] >> PIN_RXD) & 1

    # ---- pin-handshake trace --------------------------------------------
    def _tstart(self, title):
        self.trace = [title]
        self.t_t0 = time.ticks_us()
        self.t_last = -1
        self._tpoll()

    def _tmark(self, text):
        if self.trace is not None:
            self.trace.append((time.ticks_diff(time.ticks_us(), self.t_t0), text))

    def _tpoll(self):
        st = mem32[_GPIO_IN] & 0x06            # bit 1 RXD, bit 2 L_CS_B
        if st != self.t_last:
            self.t_last = st
            self.trace.append((time.ticks_diff(time.ticks_us(), self.t_t0),
                               "  lens: RXD=%d L_CS=%d" % ((st >> 1) & 1, (st >> 2) & 1)))

    def _tobserve(self, ms):
        # tight sampling loop, no display updates (they would add ms gaps)
        t0 = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t0) < ms:
            if _removed or not lens_present():
                raise LensGone()
            self._tpoll()

    def _tdump(self):
        if not self.trace:
            return
        print("---- trace:", self.trace[0])
        for t, text in self.trace[1:]:
            print("%9.3f ms  %s" % (t / 1000, text))
        print("---- end trace")
        self.trace = None

    def traced_power_up(self):
        """Power the lens with every body line parked, then raise them one at
        a time, logging what the lens does after each step."""
        d = TRACE_STEP_MS
        txd = Pin(PIN_TXD, Pin.OUT, value=0)
        self.bcs = Pin(PIN_BCS, Pin.OUT, value=0)
        self.lcs = Pin(PIN_LCS, Pin.IN)
        vdp = Pin(PIN_VD, Pin.OUT, value=1)
        Pin(PIN_RXD, Pin.IN, Pin.PULL_UP)
        S.msg = "tracing pins"
        self._tstart("power-up")
        self._tmark("body: lens power on (TXD low, B_CS low, VD idle high)")
        lens_power_on()
        self._tobserve(d[0])
        self._tmark("body: TXD high")
        txd.value(1)
        self._tobserve(d[1])
        self._tmark("body: VD pulses start (60 Hz)")
        self.vd = PWM(vdp)
        self.vd.freq(VD_FREQ)
        self.vd.duty_u16(65535 - (65535 * VD_LOW_US) // (1000000 // VD_FREQ))
        self._tobserve(d[2])
        self._tmark("body: B_CS high")
        self.bcs.value(1)
        self._tobserve(d[3])
        self._tmark("body: B_CS low")
        self.bcs.value(0)
        self._tobserve(d[4])
        self._tmark("body: UART on, 750 kbaud")
        self.set_baud(BAUD_INIT)
        self._tobserve(20)
        self._tdump()

    def _wait_level(self, test, want, timeout_ms):
        t0 = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
            if _removed or not lens_present():
                raise LensGone()
            if self.trace is not None:
                self._tpoll()
            if test() == want:
                return True
            if self.trace is None:
                self.ui.service(free_run=True)
        return False

    def pin_handshake(self, what, power_on=False):
        """Pin handshake, as measured on a SELP1650 with PIN_HS_TRACE:

        power-on (lens boots in ~35 ms; TXD and VD play no part):
          1. lens pulls RXD low, then raises L_CS_B     -> "ready"
          2. body raises B_CS_L; lens releases RXD high (~2.3 ms)
          3. body drops B_CS_L;  lens drops L_CS_B     (~0.13 ms)
        speed change (lens already idle):
          1. body raises B_CS_L; lens raises L_CS_B    (~0.2 ms)
          2. body drops B_CS_L;  lens drops L_CS_B     (~0.2 ms)
        B_CS_L is held high >= 5 ms, as on the wire captures.
        Bodies allow ~2 s per step (a7S III firmware)."""
        lcs = self.lcs.value
        rxd = self._rxd_high
        tmo = PIN_HS_TIMEOUT_MS
        log(what, ": start RXD=%d L_CS=%d" % (rxd(), lcs()))
        fail = None
        if power_on:
            if not self._wait_level(lcs, 1, tmo):
                fail = "lens never signalled ready (L_CS high)"
            self._tmark("body: B_CS high")
            self.bcs.value(1)
            if not fail and not self._wait_level(rxd, 1, tmo):
                fail = "lens did not release RXD"
        else:
            self._tmark("body: B_CS high")
            self.bcs.value(1)
            if not self._wait_level(lcs, 1, tmo):
                fail = "lens CS did not follow"
        time.sleep_ms(5)
        self._tmark("body: B_CS low")
        self.bcs.value(0)
        if not fail and not self._wait_level(lcs, 0, tmo):
            fail = "lens CS stayed high"
        if self.trace is not None:
            self._tobserve(20)
        if fail:
            log(what, ":", fail)
            if PIN_HS_STRICT:
                raise LinkError("%s: %s" % (what, fail))
            return False
        log(what, ": handshake ok")
        return True

    def set_baud(self, baud):
        if self.uart:
            self.uart.deinit()
        self.uart = UART(0, baudrate=baud, bits=8, parity=None, stop=1,
                         tx=Pin(PIN_TXD), rx=Pin(PIN_RXD),
                         rxbuf=2048, txbuf=256, timeout=0, timeout_char=0)
        self.rxd_pullup()
        self.fill = 0

    @staticmethod
    def rxd_pullup():
        # RP2040 pads reset with the pull-DOWN on, and the board has no
        # resistor on L_TO_B_RXD. A Sony body holds RXD up (it waits for it
        # to rise at power-on and fall at power-off), so do the same with
        # the internal pull-up (~50-80k).
        mem32[_PADS_GP1] = (mem32[_PADS_GP1] & ~0x0C) | 0x08
    def stop_bus(self):
        try:
            if self.uart:
                self.uart.deinit()
            if self.vd:
                self.vd.deinit()
        except Exception:
            pass
        self.uart = None
        self.vd = None

    # ---- framing ---------------------------------------------------------
    def send(self, cls, seq, mid, plen):
        """Payload must already be in self.tx[6:6+plen]."""
        n = plen + 9
        tx = self.tx
        tx[0] = 0xF0
        tx[1] = n & 0xFF
        tx[2] = n >> 8
        tx[3] = cls
        tx[4] = seq
        tx[5] = mid
        c = _csum(tx, 1, n - 3)
        tx[n - 3] = c & 0xFF
        tx[n - 2] = c >> 8
        tx[n - 1] = 0x55
        self.bcs.value(1)
        time.sleep_us(CS_LEAD_US)
        self.uart.write(self.txmv[:n])
        while not self.uart.txdone():
            pass
        time.sleep_us(CS_TRAIL_US)
        self.bcs.value(0)

    def poll_rx(self):
        u = self.uart
        if u.any() and self.fill < len(self.rx):
            n = u.readinto(self.rxmv[self.fill:])
            if n:
                self.fill += n
        buf = self.rx
        fill = self.fill
        i = 0
        while True:
            while i < fill and buf[i] != 0xF0:
                i += 1
            if fill - i < 9:
                break
            ln = buf[i + 1] | (buf[i + 2] << 8)
            if ln < 9 or ln > MAX_FRAME:
                i += 1
                continue
            if fill - i < ln:
                break
            if buf[i + ln - 1] != 0x55 or \
                    _csum(buf, i + 1, i + ln - 3) != (buf[i + ln - 3] | (buf[i + ln - 2] << 8)):
                S.bad += 1
                i += 1
                continue
            self.on_frame(buf[i + 3], buf[i + 4], buf[i + 5], i + 6, ln - 9)
            i += ln
        if i:
            rem = fill - i
            if rem > 0:
                self.rxmv[0:rem] = self.rxmv[i:fill]
            self.fill = max(rem, 0)
        elif self.fill >= len(self.rx):
            self.fill = 0       # garbage filled the buffer; start over

    def on_frame(self, cls, seq, mid, off, n):
        b = self.rx
        if cls == 0x02:
            self.reply = (mid, bytes(self.rxmv[off:off + n]))
        elif cls == 0x01:
            if mid == 0x05 and n >= 96:
                S.ap = _u16(b, off)
                S.dist = _u16(b, off + 20)
                S.flags05 = b[off + 22]
                S.focal = _u16(b, off + 24)
                S.ring = b[off + 60]
                S.switch = b[off + 62]
                S.row_lo = b[off + 77]
                S.row_hi = b[off + 78]
            elif mid == 0x06 and n >= 39:
                S.st06 = b[off]
                S.dir06 = b[off + 1]
                S.lim_lo = _u16(b, off + 7)
                S.lim_hi = _u16(b, off + 9)
                S.pos = _u16(b, off + 20)
                S.seq = seq
                S.frames += 1
                self.pending_seq = seq
                self.t_last06 = time.ticks_ms()

    # ---- the cooperative pump --------------------------------------------
    def pump(self, running=False):
        if _removed or not lens_present():
            raise LensGone()
        self.poll_rx()
        if running and self.pending_seq >= 0:
            seq = self.pending_seq
            self.pending_seq = -1
            self.send_03(seq)
            self.send_04(seq)
            self.ui.quiet_window(2)
            if self.ui.eject_req:
                # we have just closed a cycle: the bus is quiet until the
                # next VD, which is the cleanest place to leave the loop
                raise EjectRequest()
        self.ui.service(free_run=not running)
        if not running and self.ui.eject_req and S.phase in ("power", "init"):
            raise EjectRequest()    # nothing to shut down yet: just cut power

    def wait_ms(self, ms):
        t0 = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t0) < ms:
            self.pump()

    # ---- init handshake --------------------------------------------------
    def xfer(self, mid, payload, timeout_ms=INIT_TIMEOUT_MS, tries=3):
        S.msg = "msg 0x%02X" % mid
        for _ in range(tries):
            self.reply = None
            self.tx[6:6 + len(payload)] = payload
            self.send(0x02, 0x00, mid, len(payload))
            t0 = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
                self.pump()
                r = self.reply
                if r and r[0] == mid:
                    self.wait_ms(2)
                    return r[1]
        raise LinkError("no reply 0x%02X" % mid)

    def lens_supports(self, mid):
        return (self.lens_bitmap >> (mid - 1)) & 1

    def init_lens(self):
        S.phase = "init"
        # 0x01 capability bitmap: A6000 offer (IDs 0x01..0x3D)
        offer = bytearray(32)
        offer[0:8] = b"\xff\xff\xff\xff\xff\xff\xff\x1f"
        if REQUEST_LENS_NAME:
            offer[7] |= 0x40                    # bit 62 = ID 0x3F
        r = self.xfer(0x01, offer)
        self.lens_bitmap = int.from_bytes(r[0:8], "little")
        log("lens bitmap", r[0:8])

        # 0x07 identity
        r = self.xfer(0x07, b"\x00")
        if r[0] & 3 not in (1, 2):
            raise LinkError("unknown lens class %d" % r[0])
        if r[4]:
            raise LinkError("lens fw error 0x%02X" % r[4])   # A7 IV: LENS FIRMERR
        S.native = (r[0] & 3) == 1
        S.lens_id = r[9] | (r[10] << 8)
        speeds = r[1]
        log("lens class", r[0], "speeds 0x%02X" % speeds, "id 0x%04X" % S.lens_id)

        # 0x0C baud negotiation: only if the lens declared a speed in pl[1]
        speed = 2 if (speeds & 4 and MAX_SPEED >= 2) else (1 if speeds & 2 else 0)
        if speed:
            r = self.xfer(0x0C, b"\x04" if speed == 2 else b"\x02")
            if r and r[0] & 1:
                # the pin handshake runs again around the speed change
                if PIN_HS_TRACE:
                    self._tstart("speed change")
                    self._tmark("body: 0x0C reply received")
                self.set_baud(BAUD_SPEED[speed])
                self._tmark("body: UART at new speed")
                self.pin_handshake("speed change")
                self._tdump()
                log("baud", BAUD_SPEED[speed])

        self.xfer(0x0B, b"\x60\x00")

        if REQUEST_LENS_NAME and self.lens_supports(0x3F):
            try:
                r = self.xfer(0x3F, b"\x00")
                S.name = bytes(c for c in r if 32 <= c < 127).decode().strip()
            except LinkError:
                pass

        # 0x08 big descriptor (A6000 request, bit 7 of pl[1] clear)
        r = self.xfer(0x08, b"\xc2\x61\x00\x00\x00\x0c\x62\x02")
        if len(r) >= 22:
            S.ap_max = _u16(r, 0)
            S.ap_min = _u16(r, 2)
            S.fl_short = _bcd(r[16]) * 100 + _bcd(r[17])
            S.fl_long = _bcd(r[18]) * 100 + _bcd(r[19])
            f_s = _bcd(r[20]) / 10
            f_l = _bcd(r[21]) / 10
            if not S.name and S.fl_short:
                if S.fl_long:
                    S.name = "%d-%d F%.1f-%.1f" % (S.fl_short, S.fl_long, f_s, f_l)
                elif f_s:
                    S.name = "%dmm F%.1f" % (S.fl_short, f_s)
                else:
                    S.name = "%dmm" % S.fl_short
        log("0x08:", S.name, "ap", S.ap_max, S.ap_min)

        r = self.xfer(0x09, b"\x00\x00\x00\x00")
        if len(r) >= 9 and (r[7] or r[8]):
            raise LinkError("0x09 start-up info err")   # A7 IV aborts here
        self.xfer(0x0D, b"\x00")
        S.msg = "lens starting"
        # 0x10: reply bit 0 set = "not ready"; a body keeps waiting for a
        # further reply without resending
        r = self.xfer(0x10, b"\x1f" if S.native else b"\x3f",
                      timeout_ms=INIT_0x10_TIMEOUT_MS, tries=1)
        t0 = time.ticks_ms()
        while r and r[0] & 1:
            self.reply = None
            while self.reply is None or self.reply[0] != 0x10:
                if time.ticks_diff(time.ticks_ms(), t0) > INIT_0x10_TIMEOUT_MS:
                    raise LinkError("lens never ready")
                self.pump()
            r = self.reply[1]
        # 0x0A: ff 7f -> 105-byte 0x05; pl[8] = 3f -> 48-byte 0x06
        self.xfer(0x0A, b"\xff\x7f\x00\x00\x00\x00\x00\x00\x3f\x00\x00\x00\x00\x00\x00\x00")
        log("init done")

    # ---- normal loop frames ----------------------------------------------
    def send_03(self, seq):
        p = self.tx
        o = 6
        ap = S.ap_cmd or S.ap or 0x1400
        self.body0 = (self.body0 + 0x0A31) & 0xFFFF   # body-side value, meaning unknown
        p[o + 0] = self.body0 & 0xFF
        p[o + 1] = self.body0 >> 8
        p[o + 2] = 0
        first_ap = 0x1000 if self.first03 else ap
        p[o + 3] = first_ap & 0xFF
        p[o + 4] = first_ap >> 8
        p[o + 5] = ap & 0xFF                    # commanded aperture
        p[o + 6] = ap >> 8
        p[o + 7] = 0x94 if self.first03 else 0x1C
        p[o + 8] = 0
        p[o + 9] = 0
        p[o + 10] = 6                           # body cycle length
        p[o + 11] = self.cycle                  # frame within the cycle
        p[o + 12] = 0
        p[o + 13] = 0x02
        p[o + 14] = 0x00
        p[o + 15] = 0x03
        p[o + 16] = 0x01
        p[o + 17] = 0
        p[o + 18] = 0
        p[o + 19] = 0
        if OSS_FIELD:
            idx, off_v, on_v = OSS_FIELD
            p[o + idx] = on_v if S.oss_req else off_v
        plen = 20
        if S.native:                            # 23-byte native form
            p[o + 20] = 0x2F
            row = ROW_PATTERN[self.row_i]
            self.row_i = (self.row_i + 1) % len(ROW_PATTERN)
            p[o + 21] = row[0]
            p[o + 22] = row[1]
            plen = 23
        self.first03 = False
        self.cycle = (self.cycle + 1) % 6
        self.send(0x01, seq, 0x03, plen)

    def send_04(self, seq):
        p = self.tx
        o = 6
        mode = 0x81             # focus follow: lens follows its own ring
        state = 0x08
        rec = 0                 # 0 none, 1 move, 2 stop
        target = 0
        span = S.lim_hi - S.lim_lo
        want = self.ui.focus_dir if span > 0 else 0

        if want:
            vmax = max(1.0, span / (FOCUS_FULL_TRAVEL_S * VD_FREQ))
            vmin = max(1.0, span * FOCUS_CRAWL_FRACTION)
            if self.f_state != 1:
                self.f_state = 1
                self.f_target = float(S.pos)
                self.f_v = vmin
            self.f_v = min(vmax, self.f_v + (vmax - vmin) / (FOCUS_RAMP_S * VD_FREQ))
            t = self.f_target + want * self.f_v
            lead = 3 * vmax     # never run far ahead of the real position
            t = max(S.pos - lead, min(S.pos + lead, t))
            t = max(S.lim_lo, min(S.lim_hi, t))
            self.f_target = t
            target = int(t)
            mode, state, rec = 0x83, 0x40, 1
            S.focus_mode = "DRV"
        elif self.f_state == 1:
            self.f_state = 2
            self.f_stop_frames = 0
            mode, state, rec = 0x83, 0x41, 2
            S.focus_mode = "STP"
        elif self.f_state == 2:
            # stay in body-driven mode until the lens is at rest, then hand
            # focus back to the ring (a lens only switches mode at rest)
            self.f_stop_frames += 1
            mode, state = 0x83, 0x09
            if (S.dir06 == 0 and not (S.flags05 & 0x40) and self.f_stop_frames >= 3) \
                    or self.f_stop_frames > 30:
                self.f_state = 0
        else:
            S.focus_mode = "MF"

        hdr = (0x00, 0x00, 0x19, mode, 0x00, 0x00, 0x28,
               0x1F if S.lens_id >= 0x8000 else 0x00,
               0x00, 0x00, state, 0x00, 0x00)
        for k in range(13):
            p[o + k] = hdr[k]
        plen = 13
        if rec == 1:            # Move, absolute (mode 0)
            p[o + 13] = 0x1D
            p[o + 14] = target & 0xFF
            p[o + 15] = target >> 8
            p[o + 16] = 0x00
            p[o + 17] = 0x00
            plen = 18
        elif rec == 2:          # Stop
            p[o + 13] = 0x1C
            plen = 14
        self.send(0x01, seq, 0x04, plen)

    # ---- run one session -------------------------------------------------
    def run(self):
        S.phase = "power"
        S.msg = "powering up"
        if PIN_HS_TRACE:
            self.traced_power_up()      # replaces the normal handshake
            self.bcs = Pin(PIN_BCS, Pin.OUT, value=0)
        else:
            lens_power_on()
            self.start_bus()
            self.wait_ms(LENS_BOOT_MS)
            S.msg = "pin handshake"
            self.pin_handshake("power-on", power_on=True)
        self.init_lens()
        S.phase = "run"
        self.t_last06 = time.ticks_ms()
        try:
            while True:
                self.pump(running=True)
                if time.ticks_diff(time.ticks_ms(), self.t_last06) > LOOP_TIMEOUT_MS:
                    raise LinkError("lens went quiet")
        except EjectRequest:
            self.shutdown()
            raise

    def shutdown(self):
        """Graceful end of session, following the A7 IV power-off state
        machine (NEX-7 captures agree on the frames):
          1. 0x0A with an all-zero payload, wait for the reply
          2. 0x16 (payload 01), wait for any 0x16 reply; the lens parks
             (power-zoom retract, focus) *before* it replies
          3. cut the motor supply (LENS_PWR)
          4. drop B_CS_L, UART off, TXD/RXD back to plain GPIO
          5. wait for the lens to pull RXD low (body: 5 ms polls, ~30 s max)
          6. drive TXD low; then the caller cuts LOGIC_VCC"""
        self.ui.eject_req = False
        S.phase = "eject"
        S.focus_mode = "--"
        log("eject: shutting lens down")
        try:
            S.msg = "closing session"
            self.xfer(0x0A, bytes(16), tries=1)
        except LinkError:
            log("eject: no 0x0A echo")
        try:
            S.msg = "shutdown 0x16"
            # NEX-7 sends payload 01; Sony lenses answer with payload 00
            self.xfer(0x16, b"\x01", timeout_ms=SHUTDOWN_ACK_MS, tries=1)
            log("eject: 0x16 acknowledged")
        except LinkError:
            log("eject: no 0x16 ack, powering off anyway")
        pwr.init(Pin.IN)                        # 3. motor supply off
        self.bcs.value(0)                       # 4. release the bus
        self.stop_bus()
        txd = Pin(PIN_TXD, Pin.OUT, value=1)    # keep TXD idle-high for now
        Pin(PIN_RXD, Pin.IN, Pin.PULL_UP)
        S.msg = "waiting for RXD"
        if self._wait_level(self._rxd_high, 0, POWEROFF_RXD_LOW_MS):  # 5.
            log("eject: lens released RXD")
        else:
            log("eject: RXD stayed high, powering off anyway")
        txd.value(0)                            # 6. TXD low
        Pin(PIN_VD, Pin.IN)


# --------------------------------------------------------------------------
# Top level
# --------------------------------------------------------------------------
def idle_ui(ui, ms):
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < ms:
        ui.service(free_run=True)


def main():
    lens_power_off()
    ui = UI()
    while True:
        S.reset()
        # wait for a lens, debounced
        t_low = None
        while True:
            ui.service(free_run=True)
            ui.eject_req = False        # eject means nothing with no lens
            if lens_present():
                if t_low is None:
                    t_low = time.ticks_ms()
                elif time.ticks_diff(time.ticks_ms(), t_low) >= DET_DEBOUNCE_MS:
                    break
            else:
                t_low = None
        sess = Session(ui)
        try:
            sess.run()
        except LensGone:
            log("lens removed")
        except EjectRequest:
            log("lens ejected")
            S.phase = "ejected"
        except LinkError as e:
            log("link error:", e)
            S.phase = "error"
            S.msg = str(e)
        finally:
            # On removal the IRQ has already cut power and tri-stated the bus.
            sess.stop_bus()
            lens_power_off()
        if S.phase == "error":
            idle_ui(ui, 1000)   # lens stays unpowered for 1 s, then retry
        elif S.phase == "ejected":
            # stay powered off until the lens is pulled, or EJECT is pressed
            # again to reconnect the lens that is still mounted
            ui.eject_req = False
            while lens_present() and not ui.eject_req:
                ui.service(free_run=True)
            ui.eject_req = False


main()
