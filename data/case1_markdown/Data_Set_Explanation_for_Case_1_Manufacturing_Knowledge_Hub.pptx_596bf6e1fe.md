<!-- case1_doc_name: Data Set Explanation for Case 1 Manufacturing Knowledge Hub.pptx.pdf | case1_version: ISION -->

# Case 1: Manufacturing Knowledge Hub

# P&ID & Plot Plan Overview

| Data Source | P\&ID (Piping & Instrumentation Diagram) + Plot Plan                                          |
| ----------- | --------------------------------------------------------------------------------------------- |
| Purpose     | Connect process logic, field location, operations, troubleshooting, and maintenance knowledge |


<table>
  <tr>
    <th>Equipment &#x26; Flow</th>
    <th>Piping &#x26; Valve Logic</th>
    <th>Instrumentation &#x26; Control</th>
    <th>Safety &#x26; Knowledge</th>
  </tr>
<tr>
    <td>
    - Equipment list
    - Process flow paths
    - Material &#x26; utility movement
    </td>
<td>
    - Pipes &#x26; connections
    - Valves &#x26; bypasses
    - Drains and vents
    </td>
<td>
    - Sensors &#x26; transmitters
    - Control valves
    - DCS &#x26; monitoring points
    </td>
<td>
    - Trips &#x26; alarms
    - Shutdown/interlocks
    - SOPs, incidents, live data
    </td>
  </tr>
</table>

P&ID explains how the system works. Plot Plan shows where equipment is located. Together they create operational context for decision-making.

# P&ID #SET1 - **Feed / Pumping System**

## ~~What it shows~~
- Feed transfer from storage tank to reactor/process
- Pump protection logic: min-flow bypass, suction pressure, seal flush, vibration, temperature trips

## ~~What it can extract~~
- Pump, valve, line, flow, pressure, motor tags
- Trip, permissive, alarm and seal flush conditions

## ~~How it is useful~~
- Explains start-up, low-flow and suction issues
- Links logic with SOP and maintenance history

| Item                  | Tag                                                                | Description                                            |
| --------------------- | ------------------------------------------------------------------ | ------------------------------------------------------ |
| FROM STORAGE TANK     | 12-T-01                                                            |                                                        |
| Line Size             | 4"                                                                 |                                                        |
| Valve                 | XV-1201                                                            |                                                        |
| PSLL-1201             | Suction Pressure LOW-LOW<br/>Setpoint: 0.5 barg (per Cause/Effect) |                                                        |
| Instrument            | ZSO-1201                                                           | Suction OPEN                                           |
| Instrument            | PT-1201                                                            |                                                        |
| Instrument            | PI 1201                                                            |                                                        |
| Line Size             | 3"                                                                 |                                                        |
| Pump                  | GA-1201A                                                           |                                                        |
| Instrument            | PSLL 1201                                                          |                                                        |
| Instrument            | ZS                                                                 |                                                        |
| Valve                 | XV-1201A/B                                                         | 2"                                                     |
| Instrument            | NRV                                                                |                                                        |
| Line                  | 4"-HC-1002-CS02-I                                                  |                                                        |
| Valve                 | FV-1201                                                            | OPEN on Low Flow                                       |
| TRIP                  |                                                                    |                                                        |
| Line Size             | 2"                                                                 |                                                        |
| Valve                 | XV-1201A/B                                                         | 2"                                                     |
| Instrument            | FI 1201                                                            |                                                        |
| Instrument            | NRV                                                                |                                                        |
| Line                  | 4"-HC-1002-CS02-I                                                  |                                                        |
| Valve                 | FIT-1201                                                           |                                                        |
| TRIP                  | FIT-1201                                                           |                                                        |
| TRIP                  | FSL-1201                                                           | Discharge Flow LOW-LOW<br/>9 m3/h<br/>per Cause/Effect |
| TO REACTOR            | DC-4501                                                            |                                                        |
| Motor                 | M                                                                  | 30kW<br/>EQ1000012011-                                 |
| Foundation            |                                                                    | Foundation as per GA drawing                           |
| LOCAL CONTROL STATION | HS-1201                                                            | Hand Switch for Emergency Stop (per C\&E)              |
| TSHH-1201             | TT-1201<br/>(Bearing Temp Temp)                                    | TRIP -> TRIP per C\&E                                  |
| VSHH-1201             | VT-1201<br/>(Bearing Vibration)                                    | TRIP -> TRIP per C\&E                                  |


<table>
<thead>
<tr>
<th>Plan</th>
<th>Component</th>
<th>Condition</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="3"><b>API SEAL FLUSH PLANS</b><br />(API PLAN 11 + PLAN 62 (per Datasheet and OPL))</td>
</tr>
<tr>
<td colspan="3"><b>Seal Flush from discharge</b></td>
</tr>
<tr>
<td>RO-1201</td>
<td></td>
<td></td>
</tr>
<tr>
<td>RO-1201</td>
<td>PDI-1201</td>
<td>> 1.5 bar</td>
</tr>
<tr>
<td></td>
<td></td>
<td>Confirm dP > 1.5 bar</td>
</tr>
<tr>
<td></td>
<td>PDI-1201</td>
<td>PERMISSIVE</td>
</tr>
<tr>
<td colspan="3"><b>External Quench</b></td>
</tr>
<tr>
<td>N2</td>
<td></td>
<td>LINED UP</td>
</tr>
<tr>
<td>Steam</td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td>PDI-1201</td>
<td>> 1.5 bar</td>
</tr>
<tr>
<td colspan="3"><b>API PLAN 11 + PLAN 62</b><br />(per Datasheet and OPL)</td>
</tr>
<tr>
<td colspan="3"><b>API PLAN II + PLAN 62</b><br />(per Datasheet and OPL)</td>
</tr>
</tbody>
</table>

**NOTES:**
NOTE 1: This is sample data provided for CALIBER purposes only;
NOTE 2: Refer to Datasheet TJC-LLD-DS-GA-1201A for design parameters;
NOTE 3: See SEQ-1201 logic diagram.

<table>
<thead>
<tr>
<th>Legend Symbol</th>
<th>Meaning</th>
</tr>
</thead>
<tbody>
<tr>
<td>○</td>
<td>LOGIC <i>huni</i></td>
</tr>
<tr>
<td>↔</td>
<td>START PERMISSIVE</td>
</tr>
<tr>
<td>✆</td>
<td>TRIP</td>
</tr>
<tr>
<td>◇</td>
<td>Cause/Effect</td>
</tr>
<tr>
<td colspan="2">Ref. Dwg. TJC-LLD-PID-XXXX</td>
</tr>
</tbody>
</table>

# P&ID #SET 2 - **Polymer Fluid Bed Dryer**

## ~~What it shows~~
- Dryer with powder inlet/outlet, N2 purge, venting and motor operation
- Permissive and trip logic for flow, pressure, temperature, lube oil, vibration

## ~~What it can extract~~
- Dryer, centrifuge, N2 purge, vent, motor and instrument tags
- Start permissive, ESD, DCS reset and trip logic

## ~~How it is useful~~
- Explains dryer trips and operating requirements
- Connects SOPs, purge requirements and maintenance records

<table>
<thead>
<tr>
<th>Component</th>
<th>Tag</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>Powder Inlet</td>
<td>4"</td>
<td>POWDER INLET (4")</td>
</tr>
<tr>
<td>N2 Purge</td>
<td>1"</td>
<td>N2 PURGE (1")</td>
</tr>
<tr>
<td>Powder Outlet</td>
<td>4"</td>
<td>POWDER OUTLET (4")</td>
</tr>
<tr>
<td>Dryer</td>
<td>YD-2301</td>
<td>POLYMER FLUID BED DRYER</td>
</tr>
<tr>
<td>Centrifuge</td>
<td>GF-2210</td>
<td>Centrifuge</td>
</tr>
<tr>
<td>Motor</td>
<td>M</td>
<td>30kW EQ1000012011-</td>
</tr>
<tr>
<td>Foundation</td>
<td>-</td>
<td>Foundation as per GA drawing</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Instrument</th>
<th>Tag</th>
<th>Function</th>
</tr>
</thead>
<tbody>
<tr>
<td>Flow Switch</td>
<td>FV-2302</td>
<td>Trips OPEN</td>
</tr>
<tr>
<td>Flow Switch</td>
<td>FV-2302</td>
<td>trips CLOSED</td>
</tr>
<tr>
<td>Flow Switch</td>
<td>TV-2301</td>
<td>trips CLOSED</td>
</tr>
<tr>
<td>Pressure Switch</td>
<td>TSHH-2301</td>
<td>TRIP</td>
</tr>
<tr>
<td>Level Switch</td>
<td>FSLL-2302</td>
<td>EFF-1 to EFF-5</td>
</tr>
<tr>
<td>Level Switch</td>
<td>SLL-2305</td>
<td>EFF-1 to EFF-5</td>
</tr>
<tr>
<td>Temperature Switch</td>
<td>ASHH-2307</td>
<td>TRIP</td>
</tr>
<tr>
<td>Pressure Switch</td>
<td>MPR-2301</td>
<td>TRIP</td>
</tr>
<tr>
<td>Pressure Switch</td>
<td>PSL-2306</td>
<td>Lube oil to gearbox OK</td>
</tr>
<tr>
<td>Hand Switch</td>
<td>HS-1201</td>
<td>Emergency Stop (per C&#x26;E)</td>
</tr>
</tbody>
</table>

| System                    | Tag      | Condition |
| ------------------------- | -------- | --------- |
| Seal Flush from discharge | PDI-1201 | > 1.5 bar |
| External Quench           | PDI-2301 | > 1.5 bar |


**NOTE 1:** This is sample data provided for CALIBER purposes only.
**NOTE 2:** Refer to Datasheet TJC-LLD-DS-GA-1201A for design parameters.
**NOTE 3:** See SEQ-1201 logic diagram

# P&ID #SET 3 - **Catalyst Reduction Reactor & Heater**

## ~~What it shows~~
- Hydrogen injection, catalyst bed, analysis point and temperature control
- Safety-critical interlocks, permissives and high-temperature protection

## ~~What it can extract~~
- Reactor, heater, analyzer, PSV, flow, temperature and interlock tags
- Cause-and-effect logic and trip conditions

## ~~How it is useful~~
- Answers safety-critical questions with references
- Supports startup and temperature-interlock troubleshooting

| CAUSE | CAUSES                   | EFFECTS                                 |
| ----- | ------------------------ | --------------------------------------- |
| T1-T6 | N2 FLOW > 150 kg/h       | FLOW > 150 kg/h                         |
| EFF-1 | HIGH O2 OVER TEMPERATURE | TRIPS W                                 |
| EFF-2 |                          | TRIP / MAINTAIN / INCREASE FLOW ON TRIP |
| EFF-3 |                          | FLOW ON TRIP                            |
| P1-P4 | PERMISSIVE TO            | ENABLE STARTUP                          |


NOTES:
1. COORDINATE IN PLANT DWG USING METRES.
2. ELEVATIONS RELATIVE TO CHASE EL V1-40
3. EQUIPMENT SHOWN AT APPROX FOOTPRINT SCALE.
4. HAZARDOUS AREA CLASSIFICATION FOR mss MAT OLL.

# P&ID #SET 4 - **Recycle Gas Compressor System**

Chandra Asri

## ~~What it shows~~
- Recycle compressor with anti-surge protection
- Seal gas, lube oil and cooling-water support systems

## ~~What it can extract~~
- Compressor, recycle valve, trip and permissive tags
- Anti-surge logic and equipment protection data

## ~~How it is useful~~
- AI helps investigate compressor trips and root causes
- Improve reliability and operational decision-making

| Rev. | REVISION | Date. |
| ---- | -------- | ----- |
| 1    | 01       | 02    |
| 2    | –        | 02    |
| 3    | –        | –     |
| 4    | –        | –     |


| Item                                                                             |
| -------------------------------------------------------------------------------- |
| FROM STORAGE TANK 12-T-01                                                        |
| KO DRUM FA-4510                                                                  |
| XV-4501                                                                          |
| XV-4501                                                                          |
| PT-4501                                                                          |
| PI 1201                                                                          |
| KC-4501                                                                          |
| RECYCLE GAS COMPRESSOR (Two-stage, two-throw reciprocating machine (GA drawing)) |
| M                                                                                |
| GEARBOX                                                                          |
| EA-4502                                                                          |
| PSV-4502                                                                         |
| TIC-4502                                                                         |
| TIC-4503                                                                         |
| SEQ-4501                                                                         |
| FV-4502 OPEN on Low Flow                                                         |
| TO REACTOR LOOP                                                                  |
| SEAL GAS SYSTEM                                                                  |
| Nitrogen Buffer                                                                  |
| FT-4506                                                                          |
| FT-4506                                                                          |
| PRES. RED.                                                                       |
| SEQ-4501 Permissive 2                                                            |
| LUBE OIL SYSTEM                                                                  |
| N₂                                                                               |
| FORCE VALVE                                                                      |
| NRV                                                                              |
| OLL-4504 Relief Valve                                                            |
| Oil Pump                                                                         |
| PSLL-4504                                                                        |
| P1                                                                               |
| PSL-4504 Permissive 1                                                            |
| JACKET COOLING WATER                                                             |
| VT-4501                                                                          |
| FSL-4508                                                                         |
| Permissive 4                                                                     |


| Symbol  | Meaning            |
| ------- | ------------------ |
| (DCS)   | DCS                |
| (Local) | Local              |
| (P3)    | Interlock          |
| Valve   | Valve              |
| FV      | FV                 |
| (DCS)   | Local              |
| (P3)    | Interlock          |
| XV      | Valve              |
|         | Gate               |
| FV      | Globe              |
| FV      | Check              |
| ○ - ○   | Check/Check valve  |
| ○       | gate Type          |
| ↻       | Flow Transmitter   |
| ▭       | Flow Indicator     |
| →       | Line Spec          |
| →       | Line Specification |
| ----    | Line Specified     |


## LEGEND

| Symbol | Meaning          |
| ------ | ---------------- |
| ○      | LOGIC hmi        |
| ↑      | START PERMISSIVE |
| ⊥      | TRIP             |
| ✖      | CAUSE/EFFECT     |


| This is sample data provided for CALIBER purposes only<br/>Title<br/>P\&ID: RECYCLE GAS COMPRESSOR (KC-4501) SYSTEM<br/>Title<br/>Ref. Dwg.<br/>TJC-LLD-PID-4501 | This is sample data provided for CALIBER purposes only<br/>KA-4501<br/>P\&ID: RECYCLE GAS COMPRESSOR (KC-4501) SYSTEM<br/>INSTRUMENTATION & CONTROL DIAGRAM<br/>REV.<br/>02 | This is sample data provided for CALIBER purposes only<br/>P\&ID: RECYCLE GAS COMPRESSOR (KC-4501) SYSTEM<br/>INSTRUMENTATION & CONTROL DIAGRAM<br/>DATE.<br/>02 |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |


**NOTES:**
NOTE 1. All values are fictional for training.
NOTE 2. Refer to Datasheet TJC-LLD-PF-GA-4501A for design parameters.
NOTE 3. See SEQ-4501 logic diagram
Reference Drawing: Plot Plan TJC-LLD-PP-KC-4501
Reference Drawing: Interlock Logic SEQ-4501
Materials of construction.

# P&ID #SET 5 - **Solvent Heater System**

## ~~What it shows~~
- Hexane heating using steam shell-and-tube heater
- Temperature control, condensate and steam trap system

## ~~What it can extract~~
- Heater, PSV, steam valve, trap and alarm tags
- Fouling alarm and process protection information

## ~~How it is useful~~
- Helps AI support heater performance troubleshooting and fouling analysis.
- Support energy and maintenance optimization

<table>
<thead>
<tr>
<th>INTERLOCK/CONTROL LOOP FROM CAUSE AND EFFECT</th>
</tr>
<tr>
<th>TAG</th>
<th>Reference</th>
</tr>
<tr>
<td><mark>PDT-5605</mark></td>
<td>Differential > 0.7 bar fouling alarm</td>
</tr>
</thead>
<tbody>
<tr>
<th>START PERMISSIVE FROM CAUSE AND EFFECT</th>
</tr>
<tr>
<th>TAG</th>
<th>Reference</th>
</tr>
<tr>
<td><mark>PDT-5605</mark></td>
<td>Condensate trap fouling alarm</td>
</tr>
<tr>
<td><mark>TI-5604</mark></td>
<td>Condensate trap check</td>
</tr>
</tbody>
</table>

NOTES:
NOTE 1. Plot Plan PP-EA-5601
NOTE 2. Interlock Logic IL-EA-5601
NOTE 3. OPL OPL-EA-5601-04
NOTE 4. MATERIALS: SS304L, [Refer to Material Specification], SA-516-70
NOTE 5. Fictional diagram for training purposes

Ref. Dwg. TJC-LLD-PID-5601

# P&ID #SET 6 - **Separation Level Control System**

Chandra Asri

## ~~What it shows~~
- LP Separator and level-control valve system
- Instrument air, HART communication, and voting logic

## ~~What it can extract~~
- Separator, LIC, LV-6701, DVC positioner tags
- High/low level alarms, ESD actions, permissives

## ~~How it is useful~~
- Diagnose level excursions and valve issues
- Supports control valve troubleshooting, alarm interpretation, and safer operating decisions.

<table>
  <thead>
    <tr>
      <th>Permissive</th>
      <th>Permissive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Permissive 1</td>
<td>PI-6702 > 1.2 barg</td>
    </tr>
<tr>
      <td>Permissive 2</td>
<td>DVC6200 healthy</td>
    </tr>
<tr>
      <td>Permissive 3</td>
<td>HV-6701 bypass closed</td>
    </tr>
  </tbody>
</table>

# P&ID #SET7 - **Cooling Tower Fan (CT-7801) System**

## P&ID Diagram

**CT-7801** Composite Drive Shaft Arrangement

**CT-7801**
55 kW, TEFC IP56
Area Non-hazardous
Voltage 380 V/3 Ph/50 Hz
(per image_0.png)

**M**

**VSIFH-7802** Axial induced draft fan
6 FRP blades (as in <IMAGE 1>)

**FI 1201**

**PT-1201**

**PSLL 1201**

**COOLING TOWER CELL**

VENT

**COOLING TOWER**

VENT

Basin Drain

DRAIN

Drainess Drain

**P&ID: COOLING TOWER FAN (CT-7801) SYSTEM**

**NOTES:**
NOTE 1. This is sample data provided for CALIBER purpose only;
NOTE 2: Refer to Datasheet TJC-LLD-DS-GA-7801A for design parameters;
NOTE 3: See SEQ-7801 logic diagram.

<table>
<thead>
<tr>
<th colspan="7">INTERLOCK SEQ-7801</th>
</tr>
<tr>
<th>ID/Limiter</th>
<th>Tag</th>
<th>test/ act.</th>
<th colspan="4">Effects</th>
<th>Final Element / Action</th>
</tr>
<tr>
<th></th>
<th></th>
<th></th>
<th>EFF-1</th>
<th>EFF-2</th>
<th>EFF-3</th>
<th></th>
</tr>
  </thead>
  <tbody>
<tr>
<td>Fan vibration</td>
<td>VSHH-7802</td>
<td>>9 mm/s</td>
<td>1</td>
<td>X</td>
<td>T1</td>
<td>T2</td>
<td>T3</td>
<td>T4</td>
<td>Trip Fan Motor CT-7801</td>
</tr>
<tr>
<td>Fan vibration</td>
<td>VSHH-7802</td>
<td>=90 dag C</td>
<td>1</td>
<td>X</td>
<td></td>
<td>X</td>
<td></td>
<td></td>
<td>Trip Fan Motor CT-7801</td>
</tr>
<tr>
<td>Gearbox oil temp</td>
<td>TSHH-7802</td>
<td>=90 dag C</td>
<td>1</td>
<td></td>
<td></td>
<td>X</td>
<td>X</td>
<td></td>
<td>Annunciate Alarm on DCS</td>
</tr>
<tr>
<td>Gearbox oil pressure</td>
<td>PSL-7807</td>
<td>0.8 barg</td>
<td>1</td>
<td>X</td>
<td></td>
<td>X</td>
<td></td>
<td></td>
<td>Request Start of Spare Coil CT-7802</td>
</tr>
<tr>
<td>Fan motor overload</td>
<td>MPR-7801</td>
<td>MPR pickup</td>
<td>1</td>
<td></td>
<td></td>
<td></td>
<td>X</td>
<td></td>
<td>Request Start of Spare Coil CT-7802</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>→ Spare Coil P&#x26;ID</td>
</tr>
<tr>
<td colspan="5"><b>START PERMISSIVE (AND-gate)</b></td>
<td></td>
</tr>
<tr>
<td colspan="5">- LG Gearbox oil level OK<br />- LT-7804 Basin level normal<br />Basin level normal (LSL-7804)<br />- lockout release logic<br />- L Gearbox oil level OK &#x3C; Other (LSL-7804)<br />- Lockout release logic in orlff per image_0.png</td>
</tr>
  </tbody>
</table>

**LEGEND**
○ LOGIC hum/
START PERMISSIVE
TRIP
Cause Effect

Ref. Plog. TJC-LLD-PID-XXXX

## ~~What it shows~~
- Cooling tower fan, gearbox, motor and cooling cell operation
- Interlocks related to vibration, oil temperature and motor load

## ~~What it can extract~~
- Fan, gearbox, motor, vibration, temperature and permissive tags
- Trip logic, spare-cell activation logic and DCS notifications

## ~~How it is useful~~
- AI helps analyze fan trips and cooling-system reliability issues
- Assist maintenance planning for vibration, gearbox problems, oil pressure verification, and motor overload investigation.

# P&ID #SET 8 - **Solvent Fractionation System**

Chandra Asri

## ~~What it shows~~
- Solvent fractionation and reflux accumulator drum system
- Reflux pumps, level protection, venting and start permissive logic

## ~~What it can extract~~
- Accumulator drum, pumps, valves, flow and pressure tags
- SIL logic, high/low level alarms, trips and DCS alarm actions

## ~~How it is useful~~
- Explain reflux operation and fractionation upsets
- Support root-cause analysis for trips, alarms and level-control issues

| Component               | Tag                 | Description/Value                                                                |
| ----------------------- | ------------------- | -------------------------------------------------------------------------------- |
| REFLUX ACCUMULATOR DRUM | SA-516 Gr.70        | Diameter: 1600 mm<br/>T-T Volume 9.6 m3<br/>PSV set. 10 barg<br/>PCV split-range |
| Pump                    | GA-8920 A (Standby) |                                                                                  |
| Pump                    | GA-8920 B (Duty)    |                                                                                  |
| Temperature Sensor      | TSHH-1201 TT-8901   | (Searing Temp Temp)                                                              |
| Flow Indicator          | FI-8912             |                                                                                  |
| Flow Indicator          | FI-8012             |                                                                                  |
| Flow Indicator          | FI-8914             |                                                                                  |
| Flow Indicator          | FI-8915             |                                                                                  |
| Pressure Transmitter    | PT-8913             |                                                                                  |
| Level Switch            | PSLL 1201           |                                                                                  |
| Pressure Transmitter    | PT-8202             |                                                                                  |
| Pressure Indicator      | PI 1201             |                                                                                  |
| Motor                   | M                   | 30kW<br/>EQ1000089011-                                                           |
| Hand Switch             | HS-5901             | Hand Switch for Emergency Stop (per CSE)                                         |


| Input                     | Logic     | Output                                |
| ------------------------- | --------- | ------------------------------------- |
| **LSHH-8901** >85%        | 1oo2 LatC | EFF-1 -> TRIP COLUMN FEED             |
| **LSLL-8901** 15%         | 1oo2 LatC | EFF-2 -> TRIP REFLUX PUMP GA-8920 A/B |
| **PSHH-8902** > 8 barg    | 1oo2 LatC | EFF-3 -> OPEN VENT PCV-8905           |
| **HS-8901** Manual E-stop |           | EFF-4 -> DCS ALARM                    |


**Note:**
1. This is sample data provided for CALIBER purpose only
2. Refer to Datasheet TJC-LLD-GA-FA-8901
3. See SEQ-8901 logic diagram

# Maintenance History (Excel)

| WO\_Number | Notification\_No | Report\_Date   | Start\_Date     | Completion\_Date | Status          | Equipment | Equipment Tag | Functional Area | Area\_Code | Area\_Nam | Plant               | Work\_Type            | Discipline | Priority |
| ---------- | ---------------- | -------------- | --------------- | ---------------- | --------------- | --------- | ------------- | --------------- | ---------- | --------- | ------------------- | --------------------- | ---------- | -------- |
| 2          | WO-240109        | NT-2024-560424 | 6/4/2024 8:16   | 6/5/2024 8:16    | 6/6/2024 3:16   | Completed | KC-4501       | RECYCLE         | TIC-LLD-4  | 4500      | GAS RECO LINEAR LO  | Inspection Instrument | Medium     |          |
| 3          | WO-240157        | NT-2024-560614 | 6/9/2024 15:36  | 6/10/2024 16:36  | 6/11/2024 18:36 | Completed | LV-6701       | SEPARATO        | TIC-LLD-6  | 6700      | PRODUCT LINEAR LO   | Predictive            | Mechanic   | Low      |
| 4          | WO-240035        | NT-2024-560138 | 6/14/2024 8:53  | 6/15/2024 7:53   | 6/15/2024 17:05 | Completed | YD-2301       | POLYMER         | TIC-LLD-2  | 2300      | POLYMER LINEAR LO   | Calibration           | Instrument | Medium   |
| ~~5~~      | WO-240181        | NT-2024-560713 | 6/14/2024 10:58 | 6/16/2024 9:58   | 6/16/2024 18:58 | Completed | CT-7801       | COOLING         | TIC-LLD-7  | *7800*    | COOLING LINEAR LO   | Predictive            | Electrical | Low      |
| 6          | WO-240087        | NT-2024-560339 | 6/18/2024 6:27  | 6/19/2024 19:27  | 7/17/2024 9:12  | Completed | KC-4501       | RECYCLE         | TIC-LLD-4  | 4500      | GAS RECO LINEAR LO  | Corrective            | Instrument | High     |
| 7          | WO-240128        | NT-2024-560498 | 6/20/2024 6:53  | 6/20/2024 18:53  | 6/20/2024 23:23 | Completed | EA-5601       | SOLVENT         | TIC-LLD-5  | 5600      | SOLVENT LINEAR LO   | Preventive            | Instrument | Low      |
| 8          | WO-240186        | NT-2024-560733 | 6/22/2024 15:06 | 6/23/2024 20:06  | 6/24/2024 6:06  | Completed | CT-7801       | COOLING         | TIC-LLD-7  | 7800      | COOLING LINEAR LO   | Inspection            | Instrument | Medium   |
| 9          | WO-240085        | NT-2024-560332 | 6/22/2024 15:21 | 6/25/2024 8:21   | 6/27/2024 1:21  | Completed | KC-4501       | RECYCLE         | TIC-LLD-4  | 4500      | GAS RECO LINEAR LO  | Overhaul              | Mechanic   | High     |
| 10         | WO-240130        | NT-2024-560505 | 6/22/2024 16:00 | 6/24/2024 2:00   | 6/26/2024 1:00  | Completed | EA-5601       | SOLVENT         | TIC-LLD-5  | 5600      | SOLVENT LINEAR LO   | Predictive            | Electrical | Low      |
| 11         | WO-240195        | NT-2024-560767 | 7/1/2024 9:40   | 7/1/2024 15:40   | 7/2/2024 12:40  | Completed | FA-8901       | REFLUX AC       | TIC-LLD-8  | 8900      | SOLVENT LINEAR LO   | Corrective            | Mechanic   | Medium   |
| 12         | WO-240190        | NT-2024-560745 | 7/4/2024 13:15  | 7/5/2024 6:15    | 7/6/2024 16:03  | Completed | FA-8901       | REFLUX AC       | TIC-LLD-8  | 8900      | SOLVENT LINEAR LO   | Corrective            | Mechanic   | Medium   |
| 13         | WO-240177        | NT-2024-560696 | 7/5/2024 12:51  | 7/6/2024 16:51   | 7/7/2024 5:21   | Completed | CT-7801       | COOLING         | TIC-LLD-7  | 7800      | COOLING LINEAR LO   | Preventive            | Mechanic   | Low      |
| 14         | WO-240103        | NT-2024-560404 | 7/6/2024 15:25  | 7/7/2024 0:25    | 7/8/2024 14:25  | Completed | KC-4501       | RECYCLE         | TIC-LLD-4  | 4500      | GAS RECO LINEAR LO  | Predictive            | Electrical | Low      |
| 15         | WO-24056         | NT-2024-560212 | 7/9/2024 14:28  | 7/9/2024 14:28   | 7/11/2024 10:28 | Completed | DC-3401A      | CATALYST        | TIC-LLD-3  | 3400      | CATALYST LINEAR LO  | Corrective            | Instrument | High     |
| 16         | WO-240138        | NT-2024-560545 | 7/16/2024 10:36 | 7/17/2024 8:36   | 7/18/2024 13:54 | Completed | LV-6701       | SEPARATO        | TIC-LLD-6  | 6700      | PRODUCT LINEAR LO   | Corrective            | Instrument | Medium   |
| 17         | WO-240090        | NT-2024-560350 | 7/16/2024 15:48 | 7/16/2024 17:48  | 7/17/2024 9:12  | Completed | KC-4501       | RECYCLE         | TIC-LLD-4  | 4500      | GAS RECO LINEAR LO  | Calibration           | Instrument | High     |
| 18         | WO-240146        | NT-2024-560576 | 7/22/2024 13:24 | 7/21/2024 15:24  | 7/23/2024 16:24 | Completed | LV-6701       | SEPARATO        | TIC-LLD-6  | 6700      | PRODUCT LINEAR LO   | Preventive            | Mechanic   | Low      |
| 19         | WO-240202        | NT-2024-560790 | 7/21/2024 8:02  | 7/22/2024 22:02  | 7/23/2024 3:32  | Completed | FA-8901       | REFLUX AC       | TIC-LLD-8  | 8900      | SOLVENT LINEAR LO   | Preventive            | Mechanic   | Low      |
| 20         | WO-240172        | NT-2024-560673 | 7/22/2024 8:25  | 7/22/2024 20:25  | 7/23/2024 10:25 | Completed | CT-7801       | COOLING         | TIC-LLD-7  | 7800      | COOLING LINEAR LO   | Preventive            | Mechanic   | Low      |
| 21         | WO-240154        | NT-2024-560604 | 7/22/2024 14:45 | 7/22/2024 18:45  | 7/22/2024 20:45 | Completed | LV-6701       | SEPARATO        | TIC-LLD-6  | 6700      | PRODUCT LINEAR LO   | Predictive            | Electrical | Low      |
| 22         | WO-240012        | NT-2024-560049 | 7/24/2024 14:56 | 7/25/2024 0:56   | 7/26/2024 2:50  | Completed | GA-1201A      | HEXANE FI       | TIC-LLD-1  | 1200      | FEED PREF LINEAR LO | Inspection            | Instrument | Medium   |
| 23         | WO-240129        | NT-2024-560502 | 7/25/2024 8:19  | 7/28/2024 1:19   | 7/29/2024 13:19 | Completed | EA-5601       | SOLVENT         | TIC-LLD-5  | 5600      | SOLVENT LINEAR LO   | Predictive            | Electrical | Low      |
| 24         | WO-240409        | NT-2024-560184 | 7/26/2024 15:46 | 7/28/2024 18:46  | 7/29/2024 3:46  | Completed | YD-2301       | POLYMER         | TIC-LLD-2  | 2300      | POLYMER LINEAR LO   | Predictive            | Electrical | Low      |
| 25         | WO-240201        | NT-2024-560786 | 7/27/2024 8:27  | 7/28/2024 8:27   | 7/29/2024 14:57 | Completed | FA-8901       | REFLUX AC       | TIC-LLD-8  | 8900      | SOLVENT LINEAR LO   | Preventive            | Mechanic   | Low      |
| 26         | WO-240559        | NT-2024-560229 | 7/30/2024 8:23  | 8/1/2024 21:23   | 8/2/2024 14:23  | Completed | DC-3401A      | CATALYST        | TIC-LLD-3  | 3400      | CATALYST LINEAR LO  | Corrective            | Instrument | High     |
| 27         | WO-240116        | NT-2024-560455 | 7/31/2024 10:32 | 8/1/2024 4:32    | 8/2/2024 20:14  | Completed | EA-5601       | SOLVENT         | TIC-LLD-5  | 5600      | SOLVENT LINEAR LO   | Inspection            | Instrument | Medium   |
| 28         | WO-240060        | NT-2024-560235 | 8/5/2024 1:20   | 8/7/2024 15:20   | 8/8/2024 1:20   | Completed | DC-3401A      | CATALYST        | TIC-LLD-3  | 3400      | CATALYST LINEAR LO  | Corrective            | Mechanic   | High     |
| 29         | WO-240039        | NT-2024-560149 | 8/5/2024 11:31  | 8/5/2024 17:31   | 8/8/2024 0:37   | Completed | YD-2301       | POLYMER         | TIC-LLD-2  | 2300      | POLYMER LINEAR LO   | Corrective            | Instrument | High     |
| 30         | WO-240009        | NT-2024-560032 | 8/10/2024 8:01  | 8/11/2024 23:01  | 8/14/2024 0:19  | Completed | GA-1201A      | HEXANE FI       | TIC-LLD-1  | 1200      | FEED PREF LINEAR LO | Corrective            | Instrument | Medium   |


## What it shows

- Historical maintenance records for plant equipment
- Failures, inspections, preventive, predictive, calibration, and overhaul activities
- Downtime, maintenance costs, root causes, and corrective actions for each work order

## What it can extract

- Equipment reliability and failure trends
- Recurring issues, root causes, and breakdown patterns
- Downtime, maintenance cost, and spare part consumption analysis

Equipment-level maintenance history using **Equipment Tag** as the common key across datasets

## How it is useful

- Identifies high-risk and high-cost equipment
- Supports root cause and reliability analysis
- Connects maintenance history with operational and engineering data
- Enables predictive maintenance and maintenance knowledge hub use cases

----

Also please see the explanation of each column in this sheet
