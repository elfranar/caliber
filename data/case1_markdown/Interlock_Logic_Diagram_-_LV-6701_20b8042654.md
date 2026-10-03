<!-- case1_doc_name: Interlock Logic Diagram - LV-6701.pdf | case1_version: 3 -->

This is sample data provided for CALIBER purposes only SDK Polyolefin Expansion Project

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX

DOC NO: TJC-LLD-IL-LV-6701
WORK NO: BA-0256 REV: 3

**LOGIC No:** SEQ-6701 **DESCRIPTION:** **LP SEPARATOR LEVEL PROTECTION (FA-6710 / LV-6701) LOGIC** **SIL:** SIL 1 **TAG:** LV-6701 **FLOC:** TJC-LLD-6700-01

# CAUSE & EFFECT MATRIX

| ID     | INITIATOR / CAUSE (INPUT)   | TAG           | SET POINT  | VOTE | EFF-1 OPEN LV-6701 FULLY (relieve level) | EFF-2 CLOSE LV-6701 (prevent gas blow-by) | EFF-3 VENT ACTUATOR - LV-6701 FAILS CLOSED | EFF-4 ANNUNCIATE ALARM ON DCS |
| ------ | --------------------------- | ------------- | ---------- | ---- | ---------------------------------------- | ----------------------------------------- | ------------------------------------------ | ----------------------------- |
| **T1** | Separator level HIGH-HIGH   | **LSHH-6710** | > 85 %     | 1oo2 | ~~X~~                                    |                                           |                                            | ~~X~~                         |
| **T2** | Separator level LOW-LOW     | **LSLL-6710** | < 15 %     | 1oo2 |                                          | ~~X~~                                     |                                            | ~~X~~                         |
| **T3** | ESD activation (manual)     | **HS-6701**   | ESD signal | 1oo1 |                                          |                                           | ~~X~~                                      | ~~X~~                         |
| **T4** | Instrument air pressure LOW | **PSL-6702**  | < 1.0 barg | 1oo1 |                                          |                                           | ~~X~~                                      | ~~X~~                         |


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
<td>OPEN LV-6701 FULLY (relieve level)</td>
    </tr>
<tr>
      <td><b>EFF-2</b></td>
<td><b>CLOSE LV-6701 (prevent gas blow-by)</b></td>
    </tr>
<tr>
      <td>EFF-3</td>
<td>VENT ACTUATOR - LV-6701 FAILS CLOSED</td>
    </tr>
<tr>
      <td>EFF-4</td>
<td>ANNUNCIATE ALARM ON DCS</td>
    </tr>
  </tbody>
</table>

| #      | START PERMISSIVE (AND-gate)                                      | SIGNAL  |
| ------ | ---------------------------------------------------------------- | ------- |
| 1      | Instrument air available (> 1.2 barg)                            | PI-6702 |
| 2      | Positioner DVC6200 in AUTO/healthy                               | DVC6200 |
| 3      | Bypass HV-6701 closed (normal operation)                         | HV-6701 |
| \<b==> | **\*\*ALL permissives TRUE (AND) ==> START LV-6701 ENABLED\*\*** | **RUN** |


NOTES: 1. Trip set points are training values. 2. On any trip the effects marked X are actuated by the Safety PLC and annunciated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID TJC-LLD-PID-6701 for instrument loops and the Datasheet for design limits of LV-6701.
