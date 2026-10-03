<!-- case1_doc_name: P&ID_Set 8.png | case1_version: Not specified -->

8"-HC-1002-CS02-I -> TT-8911 -> OPL -> Safe drain collection vessel -> Vents and Drains details to safe vent header/Flare -> from COLUMN DA-8910

MINIMUM FLOW BYPASS -> FY-8911 OPEN on Low Flow -> 4"-HC-1002-CS02-I -> NRV

FROM TANK -> 4" -> XV-8901 -> PSV-8901 Suction Pressure LOW-LOW Setpoint: 0.5 barg (per Cause/Effect) -> PT-8202 -> PI 1201 -> 4" -> 3" -> REFLUX ACCUMULATOR DRUM SA-516 Gr.70 Diameter: 1600 mm T-T Volume 9.6 m3 PSV set. 10 barg PCV split-range

ZS -> XV-1201A/B -> 8" -> NRV -> 8"

PSLL 1201

XV-1201A/B -> 8" -> FI 8012 -> 6" -> GA-8920 A (Standby) -> NRV -> 6" -> REFLUX OUT FT-8912

GA-8920 B (Duty)

TSHH-1201 TT-8901 (Searing Temp Temp) -> PT-8913 -> NRV -> PRODUCT OUT PT-8913

PT-8913

HV-8904 HV-8904 Auto-drain vaint -> PCV-8905 Split-range -> NRV -> FI 8914 -> 2" -> BOOT DRAIN (HV-8904) Passing/ Leaking fix

FI 8915

LOCAL CONTROL STATION -> HS-5901 Hand Switch for Emergency Stop (per CSE)

M 30kW EQ1000089011- Foundation as per GA drawing

C/L ELEVATION from GA drawing 4500 mm

SEQ-8901 (SIL 1)
LSHH-8901 >85% -> 1oo2 LatC -> LOGIC -> EFF-1 -> TRIP COLUMN FEED
LSLL-8901 15% -> 1oo2 LatC -> LOGIC -> EFF-2 -> TRIP REFLUX PUMP GA-8920 A/B
PSHH-8902 > 8 barg -> 1oo2 LatC -> LOGIC -> EFF-3 -> OPEN VENT PCV-8905
HS-8901 Manual E-stop -> LOGIC -> EFF-4 -> DCS ALARM
START PERMISSIVE (AND-gate)

Note:
1. This is sample data provided for CALIBER purpose only
2. Refer to Datasheet TJC-LLD-GA-FA-8901
3. See SEQ-8901 logic diagram

LEGEND
O LOGIC (e.g., AND-gate)
Start Permissive
TRIP
Cause-Effect
Ref. Dwg. TJC-LLD-PID-XXXX
