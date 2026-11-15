<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.7.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="2" name="Route2" color="16" fill="1" visible="no" active="no"/>
<layer number="3" name="Route3" color="17" fill="1" visible="no" active="no"/>
<layer number="4" name="Route4" color="18" fill="1" visible="no" active="no"/>
<layer number="5" name="Route5" color="19" fill="1" visible="no" active="no"/>
<layer number="6" name="Route6" color="25" fill="1" visible="no" active="no"/>
<layer number="7" name="Route7" color="26" fill="1" visible="no" active="no"/>
<layer number="8" name="Route8" color="27" fill="1" visible="no" active="no"/>
<layer number="9" name="Route9" color="28" fill="1" visible="no" active="no"/>
<layer number="10" name="Route10" color="29" fill="1" visible="no" active="no"/>
<layer number="11" name="Route11" color="30" fill="1" visible="no" active="no"/>
<layer number="12" name="Route12" color="20" fill="1" visible="no" active="no"/>
<layer number="13" name="Route13" color="21" fill="1" visible="no" active="no"/>
<layer number="14" name="Route14" color="22" fill="1" visible="no" active="no"/>
<layer number="15" name="Route15" color="23" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="5" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="3" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="5" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="4" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
<layer number="255" name="Undefined" color="7" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="EMountPCB" urn="urn:adsk.wipprod:fs.file:vf.5guI13GXQBOR0JZY8zhYhw">
<packages>
<package name="EMOUNT" library_version="8">
<circle x="-0.485859375" y="-0.18333125" radius="29.249996875" width="0.1524" layer="49"/>
<wire x1="-24.236875" y1="-9.008521875" x2="-24.36698125" y2="-8.27254375" width="0.1524" layer="21"/>
<wire x1="-24.36698125" y1="-8.27254375" x2="-25.0320625" y2="-7.907734375" width="0.1524" layer="21"/>
<wire x1="-25.0320625" y1="-7.907734375" x2="-25.7313" y2="-8.1888" width="0.1524" layer="21"/>
<wire x1="-25.7313" y1="-8.1888" x2="-25.938153125" y2="-8.904096875" width="0.1524" layer="21"/>
<wire x1="-25.938153125" y1="-8.904096875" x2="-25.49685625" y2="-9.514990625" width="0.1524" layer="21"/>
<wire x1="-25.49685625" y1="-9.514990625" x2="-24.739715625" y2="-9.5614625" width="0.1524" layer="21"/>
<wire x1="-24.739715625" y1="-9.5614625" x2="-24.236875" y2="-9.008521875" width="0.1524" layer="21"/>
<wire x1="-9.378653125" y1="23.497259375" x2="-8.6426625" y2="23.627371875" width="0.1524" layer="21"/>
<wire x1="-8.6426625" y1="23.627371875" x2="-8.277846875" y2="24.292465625" width="0.1524" layer="21"/>
<wire x1="-8.277846875" y1="24.292465625" x2="-8.558925" y2="24.9917125" width="0.1524" layer="21"/>
<wire x1="-8.558925" y1="24.9917125" x2="-9.274234375" y2="25.198565625" width="0.1524" layer="21"/>
<wire x1="-9.274234375" y1="25.198565625" x2="-9.885134375" y2="24.757259375" width="0.1524" layer="21"/>
<wire x1="-9.885134375" y1="24.757259375" x2="-9.93160625" y2="24.00010625" width="0.1524" layer="21"/>
<wire x1="-9.93160625" y1="24.00010625" x2="-9.378653125" y2="23.497259375" width="0.1524" layer="21"/>
<wire x1="8.40699375" y1="-23.86395" x2="7.671003125" y2="-23.9940625" width="0.1524" layer="21"/>
<wire x1="7.671003125" y1="-23.9940625" x2="7.3061875" y2="-24.65915625" width="0.1524" layer="21"/>
<wire x1="7.3061875" y1="-24.65915625" x2="7.587265625" y2="-25.358403125" width="0.1524" layer="21"/>
<wire x1="7.587265625" y1="-25.358403125" x2="8.302575" y2="-25.56525625" width="0.1524" layer="21"/>
<wire x1="8.302575" y1="-25.56525625" x2="8.913475" y2="-25.12395" width="0.1524" layer="21"/>
<wire x1="8.913475" y1="-25.12395" x2="8.95994375" y2="-24.366796875" width="0.1524" layer="21"/>
<wire x1="8.95994375" y1="-24.366796875" x2="8.40699375" y2="-23.86395" width="0.1524" layer="21"/>
<wire x1="23.332403125" y1="8.560453125" x2="23.462509375" y2="7.824475" width="0.1524" layer="21"/>
<wire x1="23.462509375" y1="7.824475" x2="24.12759375" y2="7.4596625" width="0.1524" layer="21"/>
<wire x1="24.12759375" y1="7.4596625" x2="24.826828125" y2="7.74073125" width="0.1524" layer="21"/>
<wire x1="24.826828125" y1="7.74073125" x2="25.03368125" y2="8.456028125" width="0.1524" layer="21"/>
<wire x1="25.03368125" y1="8.456028125" x2="24.592384375" y2="9.06691875" width="0.1524" layer="21"/>
<wire x1="24.592384375" y1="9.06691875" x2="23.835246875" y2="9.11339375" width="0.1524" layer="21"/>
<wire x1="23.835246875" y1="9.11339375" x2="23.332403125" y2="8.560453125" width="0.1524" layer="21"/>
<hole x="24.175" y="8.3" drill="1.75"/>
<hole x="-9.125" y="24.35" drill="1.75"/>
<hole x="-25.08" y="-8.75" drill="1.75"/>
<hole x="8.15" y="-24.7" drill="1.75"/>
<smd name="P$1" x="-9.15" y="-17.95" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$2" x="-6.7" y="-18.9" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$3" x="-4.25" y="-19.55" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$4" x="-1.65" y="-19.9" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$5" x="0.95" y="-19.9" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$6" x="3.55" y="-19.5" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$7" x="6" y="-18.85" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$8" x="8.4" y="-17.8" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$9" x="10.6" y="-16.5" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<smd name="P$10" x="12.7" y="-14.85" dx="1.75" dy="1.75" layer="16" roundness="100"/>
<wire x1="20.988375" y1="4.624671875" x2="20.988375" y2="-4.75076875" width="0" layer="20"/>
<wire x1="20.988375" y1="-4.75076875" x2="12.988375" y2="-12.75076875" width="0" layer="20" curve="-90"/>
<wire x1="12.988375" y1="-12.75076875" x2="-13.87539375" y2="-12.75076875" width="0" layer="20"/>
<wire x1="-13.87539375" y1="-12.75076875" x2="-21.87539375" y2="-4.75076875" width="0" layer="20" curve="-90"/>
<wire x1="-21.87539375" y1="-4.75076875" x2="-21.87539375" y2="4.624671875" width="0" layer="20"/>
<wire x1="-21.87539375" y1="4.624671875" x2="-13.87539375" y2="12.624671875" width="0" layer="20" curve="-90"/>
<wire x1="-13.87539375" y1="12.624671875" x2="12.988375" y2="12.624671875" width="0" layer="20"/>
<wire x1="12.988375" y1="12.624671875" x2="20.988375" y2="4.624671875" width="0" layer="20" curve="-90"/>
<text x="-11.5" y="-18.05" size="1" layer="22" rot="MR0">LENS_GND</text>
<text x="-10" y="-20.2" size="1" layer="22" rot="MR0">LENS_PWR</text>
<text x="-5.9" y="-22.05" size="1" layer="22" rot="MR0">LOGIC_GND</text>
<text x="-2.65" y="-23.65" size="1" layer="22" rot="MR0">BODY_VD_LENS</text>
<text x="1.15" y="-25.4" size="1" layer="22" rot="MR0">LOGIC_VCC</text>
<text x="4.55" y="-21.55" size="1" layer="22" rot="MR0" align="top-right">LENS_CS_BODY</text>
<text x="7.8" y="-19.9" size="1" layer="22" rot="MR0" align="top-right">RXD</text>
<text x="10.85" y="-18.35" size="1" layer="22" rot="MR0" align="top-right">TXD</text>
<text x="9.893" y="-13.865" size="1" layer="22" rot="MR0" align="top-left">LENS_DET</text>
<text x="7.582" y="-15.561" size="1" layer="22" rot="MR0" align="top-left">BODY_CS_LENS</text>
<wire x1="-11" y1="-17.5" x2="-10.55915625" y2="-17.5" width="0.508" layer="22"/>
<wire x1="-10.55915625" y1="-17.5" x2="-10.375065625" y2="-17.684090625" width="0.508" layer="22"/>
<wire x1="-9.8" y1="-19.7" x2="-7.75" y2="-19.7" width="0.508" layer="22"/>
<wire x1="-7.75" y1="-19.7" x2="-7.65" y2="-19.6" width="0.508" layer="22"/>
<wire x1="-5.65" y1="-21.6" x2="-5.55" y2="-21.6" width="0.508" layer="22"/>
<wire x1="-5.55" y1="-21.6" x2="-4.7" y2="-20.75" width="0.508" layer="22"/>
<wire x1="-2.25" y1="-23.2" x2="-1.65" y2="-22.6" width="0.508" layer="22"/>
<wire x1="-1.65" y1="-22.6" x2="-1.65" y2="-21.1" width="0.508" layer="22"/>
<wire x1="1.2" y1="-21.2" x2="1.7" y2="-21.7" width="0.508" layer="22"/>
<wire x1="1.7" y1="-21.7" x2="1.7" y2="-24.7" width="0.508" layer="22"/>
<wire x1="4.25" y1="-22.1" x2="3.45" y2="-21.3" width="0.508" layer="22"/>
<wire x1="3.45" y1="-21.3" x2="3.45" y2="-20.75" width="0.508" layer="22"/>
<wire x1="6.6" y1="-20" x2="7.05" y2="-20.45" width="0.508" layer="22"/>
<wire x1="7.05" y1="-20.45" x2="7.3" y2="-20.45" width="0.508" layer="22"/>
<wire x1="9.2" y1="-18.6" x2="9.5" y2="-18.9" width="0.508" layer="22"/>
<wire x1="9.5" y1="-18.9" x2="10.4" y2="-18.9" width="0.508" layer="22"/>
<wire x1="10.267178125" y1="-14.380528125" x2="11.332528125" y2="-14.380528125" width="0.508" layer="22"/>
<wire x1="11.332528125" y1="-14.380528125" x2="11.557" y2="-14.605" width="0.508" layer="22"/>
<wire x1="7.874" y1="-16.002" x2="9.271" y2="-16.002" width="0.508" layer="22"/>
<wire x1="9.271" y1="-16.002" x2="9.398" y2="-16.129" width="0.508" layer="22"/>
</package>
</packages>
<symbols>
<symbol name="EMOUNT" library_version="7">
<pin name="LENS_GND" x="0" y="0" length="middle" direction="pwr"/>
<pin name="LENS_PWR" x="0" y="-5.08" length="middle" direction="pwr"/>
<pin name="LOGIC_GND" x="0" y="-10.16" length="middle" direction="pwr"/>
<pin name="BODY_VD_LENS" x="0" y="-15.24" length="middle"/>
<pin name="LOGIC_VCC" x="0" y="-20.32" length="middle" direction="pwr"/>
<pin name="LENS_CS_BODY" x="0" y="-25.4" length="middle"/>
<pin name="LENS_TO_BODY_RXD" x="0" y="-30.48" length="middle"/>
<pin name="BODY_TO_LENS_TXD" x="0" y="-35.56" length="middle"/>
<pin name="BODY_CS_LENS" x="0" y="-40.64" length="middle"/>
<pin name="LENS_XDETECT" x="0" y="-45.72" length="middle"/>
<wire x1="5.08" y1="2.54" x2="33.02" y2="2.54" width="0.254" layer="94"/>
<wire x1="33.02" y1="2.54" x2="33.02" y2="-48.26" width="0.254" layer="94"/>
<wire x1="33.02" y1="-48.26" x2="5.08" y2="-48.26" width="0.254" layer="94"/>
<wire x1="5.08" y1="-48.26" x2="5.08" y2="2.54" width="0.254" layer="94"/>
<text x="5.08" y="-50.8" size="1.778" layer="95">&gt;NAME</text>
<text x="5.08" y="-53.34" size="1.778" layer="96">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="EMOUNT" library_version="8">
<gates>
<gate name="G$1" symbol="EMOUNT" x="0" y="0"/>
</gates>
<devices>
<device name="" package="EMOUNT">
<connects>
<connect gate="G$1" pin="BODY_CS_LENS" pad="P$9"/>
<connect gate="G$1" pin="BODY_TO_LENS_TXD" pad="P$8"/>
<connect gate="G$1" pin="BODY_VD_LENS" pad="P$4"/>
<connect gate="G$1" pin="LENS_CS_BODY" pad="P$6"/>
<connect gate="G$1" pin="LENS_GND" pad="P$1"/>
<connect gate="G$1" pin="LENS_PWR" pad="P$2"/>
<connect gate="G$1" pin="LENS_TO_BODY_RXD" pad="P$7"/>
<connect gate="G$1" pin="LENS_XDETECT" pad="P$10"/>
<connect gate="G$1" pin="LOGIC_GND" pad="P$3"/>
<connect gate="G$1" pin="LOGIC_VCC" pad="P$5"/>
</connects>
<technologies>
<technology name="">
<attribute name="CATEGORY_L1" value="" constant="no"/>
<attribute name="CATEGORY_L2" value="" constant="no"/>
<attribute name="DATASHEET" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="VALUE" value="" constant="no"/>
<attribute name="VENDOR" value="" constant="no"/>
<attribute name="VPN" value="" constant="no"/>
<attribute name="PACKAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="Headers" urn="urn:adsk.eagle:library:11687645">
<description>&lt;h3&gt; PCBLayout.com - Frequently Used &lt;i&gt;Headers&lt;/i&gt;&lt;/h3&gt;

Visit us at &lt;a href="http://www.PCBLayout.com"&gt;PCBLayout.com&lt;/a&gt; for quick and hassle-free PCB Layout/Manufacturing ordering experience.
&lt;BR&gt;
&lt;BR&gt;
This library has been generated by our experienced pcb layout engineers using current IPC and/or industry standards. We &lt;b&gt;believe&lt;/b&gt; the content to be accurate, complete and current. But, this content is provided as a courtesy and &lt;u&gt;user assumes all risk and responsiblity of it's usage&lt;/u&gt;.
&lt;BR&gt;
&lt;BR&gt;
Feel free to contact us at &lt;a href="mailto:Support@PCBLayout.com"&gt;Support@PCBLayout.com&lt;/a&gt; if you have any questions/concerns regarding any of our content or services.</description>
<packages>
<package name="61301011121" urn="urn:adsk.eagle:footprint:11391897/1" library_version="3">
<pad name="1" x="-11.43" y="0" drill="1.1" shape="square"/>
<pad name="2" x="-8.89" y="0" drill="1.1"/>
<pad name="3" x="-6.35" y="0" drill="1.1"/>
<pad name="4" x="-3.81" y="0" drill="1.1"/>
<pad name="5" x="-1.27" y="0" drill="1.1"/>
<pad name="6" x="1.27" y="0" drill="1.1"/>
<pad name="7" x="3.81" y="0" drill="1.1"/>
<pad name="8" x="6.35" y="0" drill="1.1"/>
<pad name="9" x="8.89" y="0" drill="1.1"/>
<pad name="10" x="11.43" y="0" drill="1.1"/>
<wire x1="-12.7" y1="1.27" x2="-12.7" y2="-1.27" width="0.127" layer="21"/>
<wire x1="-12.7" y1="-1.27" x2="12.7" y2="-1.27" width="0.127" layer="21"/>
<wire x1="12.7" y1="-1.27" x2="12.7" y2="1.27" width="0.127" layer="21"/>
<wire x1="12.7" y1="1.27" x2="-12.7" y2="1.27" width="0.127" layer="21"/>
<wire x1="-12.7" y1="1.27" x2="-12.7" y2="-1.27" width="0.127" layer="51"/>
<wire x1="-12.7" y1="-1.27" x2="12.7" y2="-1.27" width="0.127" layer="51"/>
<wire x1="12.7" y1="-1.27" x2="12.7" y2="1.27" width="0.127" layer="51"/>
<wire x1="12.7" y1="1.27" x2="-12.7" y2="1.27" width="0.127" layer="51"/>
<wire x1="-12.95" y1="1.52" x2="-12.95" y2="-1.52" width="0.05" layer="39"/>
<wire x1="-12.95" y1="-1.52" x2="12.95" y2="-1.52" width="0.05" layer="39"/>
<wire x1="12.95" y1="-1.52" x2="12.95" y2="1.52" width="0.05" layer="39"/>
<wire x1="12.95" y1="1.52" x2="-12.95" y2="1.52" width="0.05" layer="39"/>
<circle x="-11.4" y="-1.8" radius="0.1" width="0.2" layer="21"/>
<text x="-13" y="2" size="1.778" layer="25">&gt;NAME</text>
<text x="-13" y="-4" size="1.778" layer="27">&gt;VALUE</text>
</package>
</packages>
<packages3d>
<package3d name="61301011121" urn="urn:adsk.eagle:package:11391917/2" type="model">
<packageinstances>
<packageinstance name="61301011121"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="61301011121" urn="urn:adsk.eagle:symbol:11687651/3" library_version="3">
<pin name="1" x="10.16" y="10.16" length="middle" direction="pas" rot="R180"/>
<pin name="2" x="10.16" y="7.62" length="middle" direction="pas" rot="R180"/>
<pin name="3" x="10.16" y="5.08" length="middle" direction="pas" rot="R180"/>
<pin name="4" x="10.16" y="2.54" length="middle" direction="pas" rot="R180"/>
<pin name="5" x="10.16" y="0" length="middle" direction="pas" rot="R180"/>
<pin name="6" x="10.16" y="-2.54" length="middle" direction="pas" rot="R180"/>
<pin name="7" x="10.16" y="-5.08" length="middle" direction="pas" rot="R180"/>
<pin name="8" x="10.16" y="-7.62" length="middle" direction="pas" rot="R180"/>
<pin name="9" x="10.16" y="-10.16" length="middle" direction="pas" rot="R180"/>
<pin name="10" x="10.16" y="-12.7" length="middle" direction="pas" rot="R180"/>
<wire x1="5.08" y1="12.7" x2="5.08" y2="-15.24" width="0.254" layer="94"/>
<wire x1="5.08" y1="-15.24" x2="-2.54" y2="-15.24" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-15.24" x2="-2.54" y2="12.7" width="0.254" layer="94"/>
<wire x1="-2.54" y1="12.7" x2="5.08" y2="12.7" width="0.254" layer="94"/>
<text x="-5.08" y="15.24" size="1.778" layer="95">&gt;NAME</text>
<text x="-5.08" y="-17.78" size="1.778" layer="96">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="61301011121" urn="urn:adsk.eagle:component:11687693/3" prefix="J" library_version="3">
<description>&lt;h3&gt; CONN HEADER VERT 10POS 2.54MM &lt;/h3&gt;
&lt;BR&gt;
&lt;a href="https://katalog.we-online.de/em/datasheet/6130xx11121.pdf"&gt; Manufacturer's datasheet&lt;/a&gt;</description>
<gates>
<gate name="G$1" symbol="61301011121" x="0" y="0"/>
</gates>
<devices>
<device name="" package="61301011121">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="10" pad="10"/>
<connect gate="G$1" pin="2" pad="2"/>
<connect gate="G$1" pin="3" pad="3"/>
<connect gate="G$1" pin="4" pad="4"/>
<connect gate="G$1" pin="5" pad="5"/>
<connect gate="G$1" pin="6" pad="6"/>
<connect gate="G$1" pin="7" pad="7"/>
<connect gate="G$1" pin="8" pad="8"/>
<connect gate="G$1" pin="9" pad="9"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:11391917/2"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="MANUFACTURER" value="Wurth Electronics Inc." constant="no"/>
<attribute name="CREATED_BY" value="PCBLayout.com" constant="no"/>
<attribute name="MPN" value="61301011121" constant="no"/>
<attribute name="DIGIKEY_PART_NUMBER" value="732-2670-ND" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$1" library="EMountPCB" library_urn="urn:adsk.wipprod:fs.file:vf.5guI13GXQBOR0JZY8zhYhw" deviceset="EMOUNT" device="" value="EMOUNT"/>
<part name="J1" library="Headers" library_urn="urn:adsk.eagle:library:11687645" deviceset="61301011121" device="" package3d_urn="urn:adsk.eagle:package:11391917/2"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$1" gate="G$1" x="0" y="0" smashed="yes">
<attribute name="NAME" x="5.08" y="-50.8" size="1.778" layer="95"/>
<attribute name="VALUE" x="5.08" y="-53.34" size="1.778" layer="96"/>
</instance>
<instance part="J1" gate="G$1" x="-91.44" y="-17.78" smashed="yes">
<attribute name="NAME" x="-96.52" y="-2.54" size="1.778" layer="95"/>
<attribute name="VALUE" x="-96.52" y="-35.56" size="1.778" layer="96"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="N$1" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="1"/>
<wire x1="-81.28" y1="-7.62" x2="-53.34" y2="-7.62" width="0.1524" layer="91"/>
<wire x1="-53.34" y1="-7.62" x2="-53.34" y2="0" width="0.1524" layer="91"/>
<wire x1="-53.34" y1="0" x2="0" y2="0" width="0.1524" layer="91"/>
<pinref part="U$1" gate="G$1" pin="LENS_GND"/>
</segment>
</net>
<net name="N$2" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="2"/>
<wire x1="-81.28" y1="-10.16" x2="-50.8" y2="-10.16" width="0.1524" layer="91"/>
<wire x1="-50.8" y1="-10.16" x2="-50.8" y2="-5.08" width="0.1524" layer="91"/>
<wire x1="-50.8" y1="-5.08" x2="0" y2="-5.08" width="0.1524" layer="91"/>
<pinref part="U$1" gate="G$1" pin="LENS_PWR"/>
</segment>
</net>
<net name="N$3" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="3"/>
<wire x1="-81.28" y1="-12.7" x2="-48.26" y2="-12.7" width="0.1524" layer="91"/>
<wire x1="-48.26" y1="-12.7" x2="-48.26" y2="-10.16" width="0.1524" layer="91"/>
<wire x1="-48.26" y1="-10.16" x2="0" y2="-10.16" width="0.1524" layer="91"/>
<pinref part="U$1" gate="G$1" pin="LOGIC_GND"/>
</segment>
</net>
<net name="N$4" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="4"/>
<wire x1="-81.28" y1="-15.24" x2="0" y2="-15.24" width="0.1524" layer="91"/>
<pinref part="U$1" gate="G$1" pin="BODY_VD_LENS"/>
</segment>
</net>
<net name="N$5" class="0">
<segment>
<wire x1="0" y1="-20.32" x2="-53.34" y2="-20.32" width="0.1524" layer="91"/>
<wire x1="-53.34" y1="-20.32" x2="-53.34" y2="-17.78" width="0.1524" layer="91"/>
<wire x1="-53.34" y1="-17.78" x2="-81.28" y2="-17.78" width="0.1524" layer="91"/>
<pinref part="J1" gate="G$1" pin="5"/>
<pinref part="U$1" gate="G$1" pin="LOGIC_VCC"/>
</segment>
</net>
<net name="N$6" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="6"/>
<wire x1="-81.28" y1="-20.32" x2="-55.88" y2="-20.32" width="0.1524" layer="91"/>
<wire x1="-55.88" y1="-20.32" x2="-55.88" y2="-25.4" width="0.1524" layer="91"/>
<wire x1="-55.88" y1="-25.4" x2="0" y2="-25.4" width="0.1524" layer="91"/>
<pinref part="U$1" gate="G$1" pin="LENS_CS_BODY"/>
</segment>
</net>
<net name="N$7" class="0">
<segment>
<wire x1="0" y1="-30.48" x2="-58.42" y2="-30.48" width="0.1524" layer="91"/>
<wire x1="-58.42" y1="-30.48" x2="-58.42" y2="-22.86" width="0.1524" layer="91"/>
<wire x1="-58.42" y1="-22.86" x2="-81.28" y2="-22.86" width="0.1524" layer="91"/>
<pinref part="J1" gate="G$1" pin="7"/>
<pinref part="U$1" gate="G$1" pin="LENS_TO_BODY_RXD"/>
</segment>
</net>
<net name="N$8" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="8"/>
<wire x1="-81.28" y1="-25.4" x2="-60.96" y2="-25.4" width="0.1524" layer="91"/>
<wire x1="-60.96" y1="-25.4" x2="-60.96" y2="-35.56" width="0.1524" layer="91"/>
<wire x1="-60.96" y1="-35.56" x2="0" y2="-35.56" width="0.1524" layer="91"/>
<pinref part="U$1" gate="G$1" pin="BODY_TO_LENS_TXD"/>
</segment>
</net>
<net name="N$9" class="0">
<segment>
<wire x1="0" y1="-40.64" x2="-63.5" y2="-40.64" width="0.1524" layer="91"/>
<wire x1="-63.5" y1="-40.64" x2="-63.5" y2="-27.94" width="0.1524" layer="91"/>
<wire x1="-63.5" y1="-27.94" x2="-81.28" y2="-27.94" width="0.1524" layer="91"/>
<pinref part="J1" gate="G$1" pin="9"/>
<pinref part="U$1" gate="G$1" pin="BODY_CS_LENS"/>
</segment>
</net>
<net name="N$10" class="0">
<segment>
<wire x1="0" y1="-45.72" x2="-66.04" y2="-45.72" width="0.1524" layer="91"/>
<wire x1="-66.04" y1="-45.72" x2="-66.04" y2="-30.48" width="0.1524" layer="91"/>
<wire x1="-66.04" y1="-30.48" x2="-81.28" y2="-30.48" width="0.1524" layer="91"/>
<pinref part="J1" gate="G$1" pin="10"/>
<pinref part="U$1" gate="G$1" pin="LENS_XDETECT"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="8.2" severity="warning">
Since Version 8.2, EAGLE supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports URNs for individual library
assets (packages, symbols, and devices). The URNs of those assets
will not be understood (or retained) with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports the association of 3D packages
with devices in libraries, schematics, and board files. Those 3D
packages will not be understood (or retained) with this version.
</note>
</compatibility>
</eagle>
