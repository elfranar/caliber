<!-- case1_doc_name: P&ID SET 5.png | case1_version: Not specified -->

Cold hexane in from upstream fictional pump -> GA-5610 -> BLOCK VALVE -> NRV -> FI-5601 -> N1 -> 6" -> EA-5601 - SOLVENT HEATER

MP steam in from steam header -> BLOCK -> FT-5603 -> FI-5603 -> TV-5602 Air-actuated, fails safe in a specific position -> TCV-5602 <mark>C1</mark> EFF-1 -> NRV -> VALVE <mark>C1</mark> <mark>C1</mark> EFF-1 -> N3 -> 4" -> EA-5601 - SOLVENT HEATER

EA-5601 - SOLVENT HEATER -> N2 -> 6" -> BLOCK VALVE -> TT-5602 -> TIC-5602 -> PSV-5607 Set 16 barg -> R1 -> EFF-3 -> Hot hexane out to recycle system

EA-5601 - SOLVENT HEATER -> N4 -> 3" -> PT-5605 -> PDT-5605 -> PDAH-5605 > 0.7 bar fouling alarm -> A1 -> EFF-2

ST-5604 Steam Trap Assembly -> TT-5604 -> TI-5604 -> Condensate Out To condensate system -> BLOCK -> Drains to collection vessel/safe drain -> SAFE DRAIN

> Vents to fine vent header/safe location

## LEGEND

- (DCS) INSTRUMENT BUBBLE (DCS)
- (DCS) CONTROLLER BUBBLE (DCS)
- <mark>FC FO</mark> FAILURE POSITION FAILURE POSITION (FC/O)
- Gate
- Globe
- Ball
- Non-return
- -> Line Spec.

| INTERLOCK/CONTROL LOOP FROM CAUSE AND EFFECT |                                      |
| -------------------------------------------- | ------------------------------------ |
| TAG                                          | Reference                            |
| *PDT-5605*                                   | Differential > 0.7 bar fouling alarm |


<table>
  <tr>
    <th colspan="2">START PERMISSIVE FROM CAUSE AND EFFECT</th>
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
</table>

**NOTES:**
NOTE 1. Plot Plan PP-EA-5601
NOTE 2. Interlock Logic IL-EA-5601
NOTE 3. OPL OPL-EA-5601-04
NOTE 4. MATERIALS: SS304L, [Refer to Material Specification], SA-516-70
NOTE 5. Fictional diagram for training purposes

## LEGEND

- O LOGIC hmi
- START PERMISSIVE
- TRIP
- CAUSE EFFECT

Ref. Dwg. TJC-LLD-PID-5601
