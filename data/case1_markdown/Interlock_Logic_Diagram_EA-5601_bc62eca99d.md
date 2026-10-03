<!-- case1_doc_name: Interlock Logic Diagram EA-5601.pdf | case1_version: 3 -->

This is sample data provided for CALIBER purposes only  
SDK Polyolefin Expansion Project

# INTERLOCK LOGIC DIAGRAM & CAUSE / EFFECT MATRIX

DOC NO: TJC-LLD-IL-EA-5601  
WORK NO: BA-0256 REV: 3

**LOGIC No: N/A (control loop only)**  
**DESCRIPTION: SOLVENT HEATER EA-5601 - TEMPERATURE CONTROL (no dedicated ESD trip)**  
**SIL: N/A**  
**TAG: EA-5601**  
**FLOC: TJC-LLD-5600-01**

# CAUSE & EFFECT MATRIX

| ID     | INITIATOR / CAUSE (INPUT)     | TAG           | SET POINT   | VOTE    | EFF-1 MODULATE STEAM VALVE TV-5602 | EFF-2 ANNUNCIATE HIGH dP / FOULING ALARM | EFF-3 MECHANICAL RELIEF VIA PSV-5607 |
| ------ | ----------------------------- | ------------- | ----------- | ------- | ---------------------------------- | ---------------------------------------- | ------------------------------------ |
| **C1** | Outlet temperature control    | **TIC-5602**  | SP 95 degC  | control | X                                  |                                          |                                      |
| **A1** | Tube-side dP HIGH (fouling)   | **PDAH-5605** | > 0.7 bar   | alarm   |                                    | X                                        |                                      |
| **R1** | Tube-side overpressure relief | **PSV-5607**  | set 16 barg | mech    |                                    |                                          | X                                    |


Legend: X = initiator (row) actuates that effect (column). Voting: 1oo1/1oo2/2oo3 = number of transmitters that must agree to trip.

| EFFECT ID | FINAL ELEMENT / ACTION             |
| --------- | ---------------------------------- |
| EFF-1     | MODULATE STEAM VALVE TV-5602       |
| EFF-2     | ANNUNCIATE HIGH dP / FOULING ALARM |
| EFF-3     | MECHANICAL RELIEF VIA PSV-5607     |


| #     | START PERMISSIVE (AND-gate)                             | SIGNAL       |
| ----- | ------------------------------------------------------- | ------------ |
| 1     | Solvent flow established (from GA-5610)                 | FSL upstream |
| 2     | Condensate trap draining (TI-5604 < steam T)            | TI-5604      |
| \<b=> | **ALL permissives TRUE (AND) => START EA-5601 ENABLED** | **RUN**      |


NOTES: 1. Trip set points are DUMMY training values. 2. On any trip the effects marked X are actuated by the Safety PLC and annunciated on the DCS. 3. A trip is latched and requires a manual reset once the cause has cleared and permissives are healthy. 4. Refer to P&ID TJC-LLD-PID-5601 for instrument loops and the Datasheet for design limits of EA-5601.
