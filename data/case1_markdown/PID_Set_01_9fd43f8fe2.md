<!-- case1_doc_name: PID_Set_01.png | case1_version: Not specified -->

# BATTERY LIMIT

FROM STORAGE TANK 12-T-01 --> 4" --> XV-1201 --> PSLL-1201 Suction Pressure LOW-LOW Setpoint: 0.5 barg (per Cause/Effect) --> 4" --> PI 1201 --> 4"-HC-1002-CS02-I --> FV-1201 OPEN on Low Flow --> TRIP --> MINIMUM FLOW BYPASS

TRIP --> ZSO-1201 Suction OPEN --> TRIP --> START PERMISSIVE

4"-HC-1002-CS02-I --> NRV --> 2" --> XV-1201A/B --> ZS --> GA-1201A

4"-HC-1002-CS02-I --> NRV --> 2" --> XV-1201A/B --> FI 1201 --> GA-1201A --> TO REACTOR DC-4501 FIT-1201 TRIP FSLL-1201 Discharge Flow LOW-LOW 9 m3/h per Cause/Effect

PSLL-1201 --> GA-1201A

TSHH-1201 TT-1201 (Bearing Temp Temp) --> TRIP --> TRIP per C&E

VSHH-1201 VT-1201 (Bearing Vibration) --> TRIP --> TRIP per C&E

M 30kW EQ1000012011- Foundation as per GA drawing

LOCAL CONTROLstation HS-1201 Hand Switch for Emergency Stop (per C&E)

## API SEAL FLUSH PLANS (API PLAN 11 + PLAN 62 (per Datasheet and OPL))

### Seal Flush from discharge
2" --> RO-1201 --> PDI-1201 > 1.5 bar Confirm dp > 1.5 bar --> PDI-1201 PERMISSIVE

### External Quench
N2 --> LINED UP --> Steam --> PDI-1201 > 1.5 bar

**API PLAN 11 + PLAN 62 (per Datasheet and OPL)**

**API PLAN 11 + PLAN 62 (per Datasheet and OPL)**

## NOTES:
NOTE 1: This is sample data provided for CALIBER purposes only;
NOTE 2: Refer to Datasheet TJC-LLD-DS-GA-1201A for design parameters;
NOTE 3: See SEQ-1201 logic diagram.

## LEGEND
LOGIC hum'
START PERMISSIVE
TRIP
Cause/Effect

Ref. Dwg. TJC-LLD-PID-XXXX
