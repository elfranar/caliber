<!-- case1_doc_name: P&ID SET 6.png | case1_version: Not specified -->

FISHER 667 Diaphragm periodic inspection prevents failures

HART communicator

DVC6200 positioner

# SEPARATION LEVEL CONTROL VALVE (LV-6701)

| Input     | Condition  | Logic              | Output | Action             |
| --------- | ---------- | ------------------ | ------ | ------------------ |
| LSHH-6710 | >85%       | VOTE: 1oo2         | EFF-1  | OPEN LV-6701 fully |
| LSLL-6710 | 15%        | VOTE: 1oo2         | EFF-4  | DCS Alarm          |
| HS-6701   | ESD manual | 1oo1               | EFF-3  | VENT actuator      |
| PSL-6702  | < 1.0 barg | OPL-OPL-LV-6701-07 | EFF-3  | VENT actuator      |
|           |            |                    | EFF-4  | DCS Alarm          |


**DETAILS:**
Globe Control Valve with Diaphragm Actuator (Fisher 667)
TJC-LLD-6700-01
Body: WCC
R: ASME 300#
Length: 300 mm

## LEGEND
- LOGIC DIAGRAM
- START PERMISSIVE
- TRIP
- CAUSE EFFECT
- Line Spec.

| PERMISSIVE   | PERMISSIVE            |
| ------------ | --------------------- |
| Permissive   | Permissive            |
| Permissive 1 | PI-6702 > 1.2 barg    |
| Permissive 2 | DVC6200 healthy       |
| Permissive 3 | HV-6701 bypass closed |


Ref. Drg. TJC-LLD-PID-XXXX
