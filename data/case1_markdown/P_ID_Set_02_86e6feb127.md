<!-- case1_doc_name: P&ID_Set_02.png | case1_version: Not specified -->

# P&ID; TJC-LLD-PID-2301 - DRYER SYSTEM (YD-2301)

| Item             | Tag                      | Description/Value                                                                                  |
| ---------------- | ------------------------ | -------------------------------------------------------------------------------------------------- |
| Source           | CENTRIFUGE GF-2210       | 4"                                                                                                 |
| Valve            | XV-2210                  |                                                                                                    |
| Pressure Switch  | PSLL-2303                | Matel of construction: SM400B Kadant rotary joint (per Cause/Effect)                               |
| Drayer           | YD-2301                  | POLYMER FLUID BED DRYER<br/>Chain and Sprocket SCM440 drive (per the OPL)<br/>4.0 x 8.5 m EL +6.00 |
| Motor            | M                        | 30kW EQ1000012011-                                                                                 |
| Motor Foundation |                          | Foundation as per GA drawing                                                                       |
| Pressure Switch  | MPR-2301                 |                                                                                                    |
| Pressure Switch  | MPR-2301                 |                                                                                                    |
| Control Station  | LOCAL CONTROL STATION    |                                                                                                    |
| Switch           | HS-1201                  | Hand Switch for Emergency Stop (per C\&E)                                                          |
| Reset            | DCS RESET                | EFF-3 Other permittives Lube oil to gearbox OK                                                     |
| Outlet           | POWDER OUTLET (4")       |                                                                                                    |
| Valve            | FIT-2301                 |                                                                                                    |
| Trips            | TRIP                     | TSHH-2301 Discharge Flow LOW-LOW 9 m3/h per Cause/Effect                                           |
| Flow             | N2 PURGE (1")            |                                                                                                    |
| Valve            | FV-2302                  | trips CLOSED                                                                                       |
| Flow             | POWDER INLET (4")        |                                                                                                    |
| Valve            | XV-2210                  |                                                                                                    |
| Source           | NITROGEN                 | PSL-2306 Lube oil to gearbox OK                                                                    |
| Valve            | FSSL-2302                |                                                                                                    |
| Flow             | EFF-1                    | TSHH-2301                                                                                          |
| Flow             | EFF-2                    | FSSL-2302                                                                                          |
| Flow             | EFF-3                    | SLLL-2305                                                                                          |
| Flow             | EFF-4                    | ASHH-2307                                                                                          |
| Flow             | EFF-5                    | MPR-2301                                                                                           |
| Outlet           | Dry powder to downstream |                                                                                                    |
| Switch           | START PERMISSIVE         |                                                                                                    |
| Trips            | TRIP                     | LSHH-2303                                                                                          |
| Pressure         | PDI-1201                 | > 1.5 bar Confirm dp > 1.5 bar                                                                     |
| Pressure         | PDI-2301                 | > 1.5 bar                                                                                          |
| Plan             | API PLAN 11 + PLAN 62    | (per Datasheet and OPL)                                                                            |
| Quench           | External Quench          | LINED UP                                                                                           |
| Flow             | N2                       |                                                                                                    |
| Flow             | Steam                    |                                                                                                    |


## Seal Flush from discharge

<table>
<thead>
<tr>
<th>Item</th>
<th>Tag</th>
<th>Description/Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>Valve</td>
<td>RO-2201</td>
<td></td>
</tr>
<tr>
<td>Pressure</td>
<td>PDI-1201</td>
<td>> 1.5 bar</td>
</tr>
<tr>
<td>Pressure</td>
<td>PDI-2301</td>
<td>PERMISSIVE</td>
</tr>
</tbody>
</table>

## External Quench

<table>
<thead>
<tr>
<th>Item</th>
<th>Tag</th>
<th>Description/Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>Flow</td>
<td>N2</td>
<td></td>
</tr>
<tr>
<td>Flow</td>
<td>Steam</td>
<td></td>
</tr>
<tr>
<td>Pressure</td>
<td>PDI-2301</td>
<td>> 1.5 bar</td>
</tr>
</tbody>
</table>

### LEGEND
- LOGIC
- START PERMISSIVE
- TRIP
- Cause/Effect

Ref. Dwg. TJC-LLD-PID-XXXX

**NOTE 1:** This is sample data provided for CALIBER purposes only.
**NOTE 2:** Refer to Datasheet TJC-LLD-DS-GA-1201A for design parameters.
**NOTE 3:** See SEQ-1201 logic diagram
