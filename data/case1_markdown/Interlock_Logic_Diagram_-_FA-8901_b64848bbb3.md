<!-- case1_doc_name: Interlock Logic Diagram - FA-8901.pdf | case1_version: 3 -->

This is sample data provided  
for CALIBER purposes only  

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX  

DOC NO: TJC-LLD-IL-FA-8901  
WORK NO: BA-0256 REV: 3  

**LOGIC No:** SEQ-8901  
**DESCRIPTION:** REFLUX ACCUMULATOR (FA-8901) OVERHEAD PROTECTION LOGIC  
**SIL:** SIL 1  
**TAG:** **FA-8901**  
**FLOC:** TJC-LLD-8900-01  

## CAUSE & EFFECT MATRIX  

| ID     | INITIATOR / CAUSE (INPUT) | TAG           | SET POINT | VOTE | EFF-1 TRIP COLUMN FEED (prevent carryover) | EFF-2 TRIP REFLUX PUMP GA-8920 (protect) | EFF-3 OPEN VENT PCV-8905 (relieve pressure) | EFF-4 ANNUNCIATE ALARM ON DCS |
| ------ | ------------------------- | ------------- | --------- | ---- | ------------------------------------------ | ---------------------------------------- | ------------------------------------------- | ----------------------------- |
| **T1** | Drum level HIGH-HIGH      | **LSHH-8901** | > 85 %    | 1oo2 | ~~X~~                                      |                                          |                                             | ~~X~~                         |
| **T2** | Drum level LOW-LOW        | **LSLL-8901** | < 15 %    | 1oo2 |                                            | ~~X~~                                    |                                             | ~~X~~                         |
| **T3** | Drum pressure HIGH-HIGH   | **PSHH-8902** | > 8 barg  | 1oo2 |                                            |                                          | ~~X~~                                       | ~~X~~                         |
| **T4** | Emergency stop (manual)   | **HS-8901**   | Manual    | 1oo1 | ~~X~~                                      | ~~X~~                                    | ~~X~~                                       | ~~X~~                         |


  

Legend: X = initiator (row) actuates that effect (column). Voting: 1oo1/1oo2/2oo3 = number of transmitters that must agree to trip.  

<table>
  <tr>
    <th>EFFECT ID</th>
    <th>FINAL ELEMENT / ACTION</th>
  </tr>
<tr>
    <td>EFF-1</td>
<td>TRIP COLUMN FEED (prevent carryover)</td>
  </tr>
<tr>
    <td><b>EFF-2</b></td>
<td><b>TRIP REFLUX PUMP GA-8920 (protect)</b></td>
  </tr>
<tr>
    <td>EFF-3</td>
<td>OPEN VENT PCV-8905 (relieve pressure)</td>
  </tr>
<tr>
    <td><b>EFF-4</b></td>
<td><b>ANNUNCIATE ALARM ON DCS</b></td>
  </tr>
</table>

| #     | START PERMISSIVE (AND-gate)                             | SIGNAL    |
| ----- | ------------------------------------------------------- | --------- |
| 1     | Level in normal band (20-80%)                           | LT-8901   |
| 2     | N2 blanket healthy                                      | PT-8902   |
| 3     | Boot not flooded                                        | LT-8903   |
| 4     | No active trip / reset done                             | DCS reset |
| \<b=> | **ALL permissives TRUE (AND) => START FA-8901 ENABLED** | **RUN**   |


  

NOTES: 1. Trip set points are DUMMY training values. 2. On any trip the effects marked X are actuated by the Safety PLC and annunciated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID; TJC-LLD-PID-8901 for instrument loops and the Datasheet for design limits of FA-8901.
