<!-- case1_doc_name: Interlock Logic Diagram - CT-7801.pdf | case1_version: 3 -->

**This is sample data provided**
**for CALIBER purposes only**

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX

DOC NO: TJC-LLD-IL-CT-7801
WORK NO: BA-0256 REV: 3

**LOGIC No: SEQ-7801** DESCRIPTION: **COOLING TOWER FAN (CT-7801) SHUTDOWN LOGIC** SIL: **SIL 1** TAG: **CT-7801** FLOC: TJC-LLD-7800-01

# CAUSE & EFFECT MATRIX

| ID | INITIATOR / CAUSE (INPUT)         | TAG           | SET POINT  | VOTE | EFF-1 TRIP FAN MOTOR CT-7801 | EFF-2 ANNUNCIATE ALARM ON DCS | EFF-3 REQUEST START OF SPARE CELL CT-7802 |
| -- | --------------------------------- | ------------- | ---------- | ---- | ---------------------------- | ----------------------------- | ----------------------------------------- |
| T1 | Fan/gearbox vibration HIGH-HIGH   | **VSHH-7802** | > 9 mm/s   | 1oo1 | ~~X~~                        | ~~X~~                         | ~~X~~                                     |
| T2 | Gearbox oil temperature HIGH-HIGH | **TSHH-7803** | > 90 degC  | 1oo1 | ~~X~~                        | ~~X~~                         | ~~X~~                                     |
| T3 | Gearbox oil pressure LOW          | **PSL-7807**  | < 0.8 barg | 1oo1 | ~~X~~                        | ~~X~~                         | ~~X~~                                     |
| T4 | Fan motor overload                | **MPR-7801**  | MPR pickup | 1oo1 | ~~X~~                        | ~~X~~                         | ~~X~~                                     |


Legend: X = initiator (row) actuates that effect (column). Voting: 1oo1/1oo2/2oo3 = number of transmitters that must agree to trip.

<table>
<thead>
<tr>
<th>EFFECT ID</th>
<th>FINAL ELEMENT / ACTION</th>
</tr>
</thead>
<tbody>
<tr>
<td>EFF-1</td>
<td>TRIP FAN MOTOR CT-7801</td>
</tr>
<tr>
<td>EFF-2</td>
<td><b>ANNUNCIATE ALARM ON DCS</b></td>
</tr>
<tr>
<td>EFF-3</td>
<td>REQUEST START OF SPARE CELL CT-7802</td>
</tr>
</tbody>
</table>

| #     | START PERMISSIVE (AND-gate)                             | SIGNAL     |
| ----- | ------------------------------------------------------- | ---------- |
| 1     | Gearbox oil level OK                                    | LG gearbox |
| 2     | Basin level normal (>= LSL-7804)                        | LT-7804    |
| 3     | No fan lockout / maintenance key released               | lockout    |
| \<b=> | **ALL permissives TRUE (AND) => START CT-7801 ENABLED** | **RUN**    |


NOTES: 1. Trip set points are DUMMY training values. 2. On any trip the effects marked X are actuated by the Safety PLC and annunciated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID; TJC-LLD-PID-7801 for instrument loops and the Datasheet for design limits of CT-7801.
