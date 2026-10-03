<!-- case1_doc_name: Interlock Logic Diagram DC-3401A.pdf | case1_version: 3 -->

This is sample data provided for **CALIBER** purposes only SDK Polyolefin Expansion Project

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX

DOC NO: TJC-LLD-IL-DC-3401A  
WORK NO: BA-0256 REV: 3

**LOGIC No: SEQ-3401**  
**DESCRIPTION: CATALYST REDUCTION REACTOR (DC-3401A) + HEATER EA-3401 LOGIC**  
**SIL: SIL 2**  
**TAG: **DC-3401A** FLOC: TJC-LLD-3400-01**

## CAUSE & EFFECT MATRIX

| ID | INITIATOR / CAUSE (INPUT)                | TAG            | SET POINT          | VOTE | EFF-1 TRIP HEATER EA-3401 | EFF-2 CLOSE H2 INJECTION FV-3403 | EFF-3 OPEN REACTOR VENT PV-3404 | EFF-4 MAINTAIN / INCREASE N2 FV-17343 | EFF-5 ANNUNCIATE ALARM ON DCS |
| -- | ---------------------------------------- | -------------- | ------------------ | ---- | ------------------------- | -------------------------------- | ------------------------------- | ------------------------------------- | ----------------------------- |
| T1 | Bed temperature HIGH-HIGH                | **TSHH-3401**  | > 230 degC         | 2oo3 | ×                         | ×                                |                                 | ×                                     | ×                             |
| T2 | Reactor pressure HIGH-HIGH               | **PSHH-3404**  | > 5 barg           | 1oo2 |                           | ×                                | ×                               |                                       | ×                             |
| T3 | Outlet O2 HIGH during H2 (inerting fail) | **AI-3401**    | > 100 ppm          | 1oo1 |                           | ×                                |                                 | ×                                     | ×                             |
| T4 | Nitrogen carrier flow LOW-LOW            | **FSLL-17343** | < 150 kg/h         | 1oo1 | ×                         | ×                                |                                 |                                       | ×                             |
| T5 | Heater element over-temperature          | **EHT-3401**   | skin TC > 260 degC | 1oo1 | ×                         |                                  |                                 |                                       | ×                             |
| T6 | Emergency stop (manual)                  | **HS-3401**    | Manual             | 1oo1 | ×                         | ×                                | ×                               |                                       | ×                             |


Legend: × = initiator (row) actuates that effect (column). Voting: 1oo1/1oo2/2oo3 = number of transmitters that must agree to trip.

<table>
  <tr>
    <th>EFFECT ID</th>
    <th>FINAL ELEMENT / ACTION</th>
  </tr>
<tr>
    <td>EFF-1</td>
<td>TRIP HEATER EA-3401</td>
  </tr>
<tr>
    <td>EFF-2</td>
<td>CLOSE H2 INJECTION FV-3403</td>
  </tr>
<tr>
    <td>EFF-3</td>
<td>OPEN REACTOR VENT PV-3404</td>
  </tr>
<tr>
    <td>EFF-4</td>
<td>MAINTAIN / INCREASE N2 FV-17343</td>
  </tr>
<tr>
    <td>EFF-5</td>
<td>ANNUNCIATE ALARM ON DCS</td>
  </tr>
</table>

<table>
  <tr>
    <th>#</th>
    <th>START PERMISSIVE (AND-gate)</th>
    <th>SIGNAL</th>
  </tr>
<tr>
    <td>1</td>
<td>O2 free / inerting done (AI-3401 &#x3C; 100 ppm)</td>
<td>AI-3401</td>
  </tr>
<tr>
    <td>2</td>
<td>N2 carrier flow established (> 150 kg/h)</td>
<td>FT-17343</td>
  </tr>
<tr>
    <td>3</td>
<td>Bed homogeneous 120 degC (all TE within 15 degC)</td>
<td>TE-3401</td>
  </tr>
<tr>
    <td>4</td>
<td>No active trip / reset done</td>
<td>DCS reset</td>
  </tr>
<tr>
    <td>&#x3C;b=>></td>
<td><b>ALL permissives TRUE (AND) => START DC-3401A ENABLED</b></td>
<td><b>RUN</b></td>
  </tr>
</table>

NOTES: 1. Trip set points are DUMMY training values. 2. On any trip the effects marked X are actuated by the Safety PLC and annunciated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID TJC-LLD-PID-3401 for instrument loops and the Datasheet for design limits of DC-3401A.
