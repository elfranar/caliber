<!-- case1_doc_name: Interlock Logic Diagram KC-4501.pdf | case1_version: 3 -->

SDK Polyolefin Expansion Project

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX

DOC NO: TJC-LLD-IL-KC-4501
WORK NO: BA-0256 REV: 3

**LOGIC No: SEQ-4501** **DESCRIPTION: RECYCLE GAS COMPRESSOR (KC-4501) SHUTDOWN LOGIC** **SIL: SIL 2** **TAG: **KC-4501**** **FLOC: TJC-LLD-4500-01**

## CAUSE & EFFECT MATRIX

| ID | INITIATOR / CAUSE (INPUT)       | TAG           | SET POINT  | VOTE | EFF-1 TRIP COMPRESSOR MOTOR KC-4501 | EFF-2 OPEN ANTI-SURGE RECYCLE FV-4502 | EFF-3 CLOSE SUCTION XV-4501 | EFF-4 MAINTAIN SEAL GAS N2 | EFF-5 ANNUNCIATE ALARM ON DCS |
| -- | ------------------------------- | ------------- | ---------- | ---- | ----------------------------------- | ------------------------------------- | --------------------------- | -------------------------- | ----------------------------- |
| T1 | Lube oil pressure LOW-LOW       | **PSLL-4504** | < 1.5 barg | 2oo3 | X                                   | X                                     | X                           |                            | X                             |
| T2 | Discharge temperature HIGH-HIGH | **TSHH-4503** | > 140 degC | 1oo1 | X                                   | X                                     |                             |                            | X                             |
| T3 | Discharge pressure HIGH-HIGH    | **PSHH-4502** | > 14 barg  | 1oo2 | X                                   | X                                     |                             |                            | X                             |
| T4 | Crosshead vibration HIGH-HIGH   | **VSHH-4505** | > 11 mm/s  | 1oo2 | X                                   | X                                     | X                           |                            | X                             |
| T5 | Suction KO drum level HIGH-HIGH | **LSHH-4510** | > 80 %     | 1oo1 | X                                   |                                       | X                           |                            | X                             |
| T6 | Suction pressure LOW-LOW        | **PSLL-4501** | < 0.3 barg | 1oo1 | X                                   | X                                     |                             |                            | X                             |


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
<td>TRIP COMPRESSOR MOTOR KC-4501</td>
</tr>
<tr>
<td>EFF-2</td>
<td><b>OPEN ANTI-SURGE RECYCLE FV-4502</b></td>
</tr>
<tr>
<td>EFF-3</td>
<td>CLOSE SUCTION XV-4501</td>
</tr>
<tr>
<td>EFF-4</td>
<td><b>MAINTAIN SEAL GAS N2</b></td>
</tr>
<tr>
<td>EFF-5</td>
<td>ANNUNCIATE ALARM ON DCS</td>
</tr>
</tbody>
</table>

| #     | START PERMISSIVE (AND-gate)                             | SIGNAL    |
| ----- | ------------------------------------------------------- | --------- |
| 1     | Lube oil pressure OK (> 2 barg)                         | PSLL-4504 |
| 2     | Seal gas established                                    | FT-4506   |
| 3     | KO drum level normal (< 50%)                            | LT-4510   |
| 4     | Jacket water flow OK                                    | FSL-4508  |
| 5     | No active trip / reset done                             | DCS reset |
| \<b=> | **ALL permissives TRUE (AND) => START KC-4501 ENABLED** | **RUN**   |


NOTES: 1. Trip set points are DUMMY training values. 2. On any trip the effects marked X are actuated by the Safety PLC and annunciated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID TJC-LLD-PID-4501 for instrument loops and the Datasheet for design limits of KC-4501.
