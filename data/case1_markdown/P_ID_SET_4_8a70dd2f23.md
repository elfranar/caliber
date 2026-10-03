<!-- case1_doc_name: P&ID SET 4.png | case1_version: ISION -->

| Rev. | REVISION | Date. |
| ---- | -------- | ----- |
| 1    | 01       | 02    |
| 2    | -        | 02    |
| 3    | -        | -     |
| 4    | -        | -     |


FROM STORAGE TANK 12-T-01

KO DRUM FA-4510

6"

XV-4501

3"

START PERMISSIVE

TRIP

PSLL-4501 Suction OPEN

PT-4501

PI 1201

SEQ-4501 Permissive 3

LT-4510

4"

XV-4501

KC-4501

RECYCLE GAS COMPRESSOR (Two-stage, two-throw reciprocating machine (GA drawing)

M GEARBOX

4"

KC-4501

N2, 4"

NRV

XV-4501

Cooling Water

6"

EA-4502 SS

PSV-4502

TIC-4502

TIC-4503

PSV-4502

TIC-4503

PSV-4502

N3, 4"

DISCHARGE

4"

4"-HC-602-CS021

TRIP

ANTI-SURGE RECYCLE CONTROL VALVING.

SEQ-4501

TRIP

FV-4502 OPEN on Low Flow

3"-HC-1002-CS021

TO REACTOR LOOP

|                 | SEAL GAS SYSTEM       |
| --------------- | --------------------- |
| Nitrogen Buffer | 1"                    |
| FT-4506         |                       |
| FT-4506         |                       |
| PRES. RED.      | SEQ-4501 Permissive 2 |


|                       | LUBE OIL SYSTEM       |
| --------------------- | --------------------- |
| N₂                    |                       |
| NRV                   |                       |
| FORCE VALVE           |                       |
| OLL-4504 Relief Valve |                       |
| PSLL-4504             |                       |
| P1                    | PSL-4504 Permissive 1 |


JACKET COOLING WATER

VT-4501

FSL-4508

Permissive 4

| LEGEND |                    |
| ------ | ------------------ |
| DCS    | DCS                |
| Local  | Local              |
| P3     | Interlock          |
| Valve  | gate Type          |
| FV     | XV Valve           |
| FV     | Gate               |
|        | Flow Transmitter   |
|        | Flow Indicator     |
|        | Line Spec          |
|        | Line Specification |
|        | Line Specified     |
|        | Check/Check valve  |


NOTES:
NOTE 1. All values are fictional for training.
NOTE 2. Refer to Datasheet TJC-LLD-PF-GA-4501A for design parameters.
NOTE 3. See SEQ-4501 logic diagram
Reference Drawing: Plot Plan TJC-LLD-PP-KC-4501
Reference Drawing: Interlock Logic SEQ-4501
Materials of construction.

|   | LOGIC hmi        |
| - | ---------------- |
|   | START PERMISSIVE |
|   | TRIP             |
|   | CAUSE/EFFECT     |


| This is sample data provided for CALIBER purposes only |                                   |          |
| ------------------------------------------------------ | --------------------------------- | -------- |
| TITLE                                                  | **KA-4501**                       |          |
| **P\&ID: RECYCLE GAS COMPRESSOR (KC-4501) SYSTEM**     |                                   |          |
| TITLE                                                  | INSTRUMENTATION & CONTROL DIAGRAM |          |
| Ref. Dwg. TJC-LLD-PID-4501                             | REV. 02                           | DATE. 02 |
