<!-- case1_doc_name: Interlock Logic Diagram - YD-2301.pdf | case1_version: 3 -->

This is sample data provided for CALIBER purposes only
SDK Polyolefin Expansion Project

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX

DOC NO: TJC-LLD-IL-YD-2301
WORK NO: BA-0256 REV: 3

**LOGIC No: SEQ-5500**
**DESCRIPTION: DRYER SYSTEM (YD-2301) SHUTDOWN LOGIC**
**SIL: SIL 2**
**TAG: YD-2301**
**FLOC: TJC-LLD-2300-01**

# CAUSE & EFFECT MATRIX

| ID     | INITIATOR / CAUSE (INPUT)       | TAG           | SET POINT  | VOTE | EFF-1 TRIP DRUM DRIVE MOTOR | EFF-2 CLOSE STEAM INLET TV-2301 | EFF-3 TRIP CENTRIFUGE FEED GF-2210 | EFF-4 OPEN N2 PURGE FV-2302 (max inert) | EFF-5 ANNUNCIATE ALARM ON DCS |
| ------ | ------------------------------- | ------------- | ---------- | ---- | --------------------------- | ------------------------------- | ---------------------------------- | --------------------------------------- | ----------------------------- |
| **T1** | Outlet temperature HIGH-HIGH    | **TSHH-2301** | > 125 degC | 1oo1 | X                           | X                               |                                    |                                         | X                             |
| **T2** | Nitrogen purge flow LOW-LOW     | **FSLL-2302** | < 200 kg/h | 2oo3 | X                           | X                               |                                    | X                                       | X                             |
| **T3** | Inlet chute level HIGH-HIGH     | **LSHH-2303** | > 90 %     | 1oo1 |                             |                                 | X                                  |                                         | X                             |
| **T4** | Drum speed LOW-LOW (chain slip) | **SSLL-2305** | < 1 rpm    | 1oo1 |                             | X                               |                                    |                                         | X                             |
| **T5** | Vent O2 HIGH-HIGH               | **ASHH-2307** | > 8 % O2   | 1oo2 | X                           | X                               |                                    | X                                       | X                             |
| **T6** | Drive motor overload            | **MPR-2301**  | MPR pickup | 1oo1 | X                           | X                               |                                    |                                         | X                             |


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
<td>TRIP DRUM DRIVE MOTOR</td>
    </tr>
<tr>
      <td>EFF-2</td>
<td>CLOSE STEAM INLET TV-2301</td>
    </tr>
<tr>
      <td>EFF-3</td>
<td>TRIP CENTRIFUGE FEED GF-2210</td>
    </tr>
<tr>
      <td>EFF-4</td>
<td>OPEN N2 PURGE FV-2302 (max inert)</td>
    </tr>
<tr>
      <td>EFF-5</td>
<td>ANNUNCIATE ALARM ON DCS</td>
    </tr>
  </tbody>
</table>

| #     | START PERMISSIVE (AND-gate)                             | SIGNAL    |
| ----- | ------------------------------------------------------- | --------- |
| 1     | Nitrogen inerting established (O2 < 5%)                 | AT-2307   |
| 2     | Steam condensate drain open                             | ZSO-2304  |
| 3     | Lube oil to gearbox OK                                  | PSL-2306  |
| 4     | No active trip / reset done                             | DCS reset |
| \<b=> | **ALL permissives TRUE (AND) => START YD-2301 ENABLED** | **RUN**   |


Notes: 1. Trip set points are DUMMY training values. 2. On any trip the effects marked X are actuated by the Safety PLC and annunciated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID; TJC-LLD-PID-2301 for instrument loops and the Datasheet for design limits of YD-2301.
