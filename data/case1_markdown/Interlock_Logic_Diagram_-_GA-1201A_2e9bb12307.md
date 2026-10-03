<!-- case1_doc_name: Interlock Logic Diagram - GA-1201A.pdf | case1_version: 3 -->

This is sample data provided for CALIBER purposes only
SDK Polyolefin Expansion Project

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX

DOC NO: TJC-LLD-IL-GA-1201A
WORK NO: BA-0256 REV: 3

**LOGIC No: SEQ-1201**
**DESCRIPTION: HEXANE FEED PUMP (GA-1201A/B) SHUTDOWN LOGIC**
**SIL: SIL 1**
**TAG: GA-1201A** **FLOC: TJC-LLD-1200-01**

# CAUSE & EFFECT MATRIX

| ID | INITIATOR / CAUSE (INPUT)         | TAG           | SET POINT         | VOTE | EFF-1 TRIP PUMP MOTOR GA-1201A | EFF-2 CLOSE DISCHARGE XV-1201 | EFF-3 OPEN MIN-FLOW FV-1201 | EFF-4 ANNUNCIATE ALARM ON DCS | EFF-5 START STANDBY PUMP GA-1201B (auto) |
| -- | --------------------------------- | ------------- | ----------------- | ---- | ------------------------------ | ----------------------------- | --------------------------- | ----------------------------- | ---------------------------------------- |
| T1 | Suction pressure LOW-LOW          | **PSLL-1201** | < 0.5 barg        | 2oo3 | X                              | X                             |                             | X                             | X                                        |
| T2 | Discharge flow LOW-LOW (min flow) | **FSLL-1201** | < 9 m3/h for 30 s | 1oo1 | X                              |                               | X                           | X                             | X                                        |
| T3 | Bearing vibration HIGH-HIGH       | **VSHH-1201** | > 7.1 mm/s RMS    | 1oo2 | X                              | X                             |                             | X                             | X                                        |
| T4 | Bearing temperature HIGH-HIGH     | **TSHH-1201** | > 95 degC         | 1oo1 | X                              | X                             |                             | X                             |                                          |
| T5 | Motor overload / electrical fault | **MPR-1201**  | MPR relay pickup  | 1oo1 | X                              | X                             |                             | X                             | X                                        |
| T6 | Local/DCS emergency stop          | **HS-1201**   | Manual            | 1oo1 | X                              | X                             |                             | X                             |                                          |


Legend: **X** = initiator (row) actuates that effect (column). Voting: 1oo1/1oo2/2oo3 = number of transmitters that must agree to trip.

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
<td>TRIP PUMP MOTOR GA-1201A</td>
</tr>
<tr>
<td>EFF-2</td>
<td>CLOSE DISCHARGE XV-1201</td>
</tr>
<tr>
<td>EFF-3</td>
<td>OPEN MIN-FLOW FV-1201</td>
</tr>
<tr>
<td>EFF-4</td>
<td>ANNUNCIATE ALARM ON DCS</td>
</tr>
<tr>
<td>EFF-5</td>
<td>START STANDBY PUMP GA-1201B (auto)</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>#</th>
<th>START PERMISSIVE (AND-gate)</th>
<th>SIGNAL</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Suction valve OPEN</td>
<td>ZSO-1201</td>
</tr>
<tr>
<td>2</td>
<td>Seal flush established (dP > 1.5 bar)</td>
<td>PDI-1201</td>
</tr>
<tr>
<td>3</td>
<td>Min-flow valve OPEN</td>
<td>ZSO-1202</td>
</tr>
<tr>
<td>4</td>
<td>No active trip / reset done</td>
<td>DCS reset</td>
</tr>
<tr>
<td>&#x3C;b=></td>
<td><b>**ALL permissives TRUE (AND) => START GA-1201A ENABLED**</b></td>
<td><b>RUN</b></td>
</tr>
</tbody>
</table>

NOTES: 1. Trip set points are DUMMY training values. 2. On any trip the effects marked X are actuated by the Safety PLC and announcated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID; TJC-LLD-PID-1201 for instrument loops and the Datasheet for design limits of GA-1201A.
