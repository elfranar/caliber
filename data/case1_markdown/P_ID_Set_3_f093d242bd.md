<!-- case1_doc_name: P&ID Set 3.png | case1_version: Not specified -->

# CATALYST REDUCTION REACTOR DC-3401A

## Main Reactor Components
- TOP MANWAY LOADING
- FIXED CATALYST
  - SAMPLE SHELL
  - Pd/Al2O3 CATALYST BED
  - SUPPORT AND HOLD-DOWN GRID
  - TOP MANWAY (M1)
  - BOTTOM MANWAY (M2)
  - MULTIPoint THERMOCOUPLE TE-3401 (8 POINTS)
- INLET DISTRIBUTOR
- TOP SUPPORT
- SKIRT SUPPORT
- UNLOADING

## Piping and Valves
- **FT 17343** FIT-12am
- **FI 17343**
- **FV-17343** FC/FO
- **T4**
- **CS**
- **BYPASS**
- **4"-HC-3401-CS02-I**
- **N1**
- **N3**
- **PSV-3401** Set, 6 barg
- **4"-HC-3401-CS02-I**
- **AI-3401**

## Interlocks
- **Interlock T4**
  - N2 FLOW > 150 kg/h
  - MAINTAIN / INCREASE FLOW ON TRIP
- **TSHH-3401**
  - High-High > 230 degC
- **Interlock T1**
  - 2oo3 VOTING
- **T1**
  - 2oo3 voting
- **Interlock T3**
  - HIGH O2 (> 100 ppm)
  - I2 (INERTING FAIL)
- **Interlock T1**
  - PERMISSIVE TO ENABLE STARTUP
- **PSHH-3404**
  - High-High > 5 barg
- **Interlock T2**
  - NORMALLY CLOSED, TRIPS ON HIGH PRESSURE

## Inlet and Outlet
- **H2 INJECTION**
  - **H2**
  - **FT DCS**
  - **FT-3403** FT-3403
  - **FI DCS**
  - **FV-3403** FC/FO
  - **EFF-2**
  - **Interlock EFF**
    - CLOSURE ON TRIP
- **ANALYSIS**
- **SAMPLE CS**

## In-Line Heater EA-3401
- **SKIN THERMOCOUPLE**
- **HS-3401** EMERGENCY STOP
- **TSHH-3401** (High >230 degC)
- **TIC 17343**
- **4"-HC-3401-CS02-I**
- **CS, SS Cladding**
- **4"-HC-3401-CS03-IE**
- **PV-3404** NORMALLY CLOSED TRIPS OPEN
- **EFF-3**
- **FV-3403** (FC/FO)
- **TRIM GAS OR ANALYSIS**

## Table: SEQ-3401

| CAUSE | CAUSES                   | EFFECTS                                 |
| ----- | ------------------------ | --------------------------------------- |
| T1-T6 | N2 FLOW > 150 kg/h       | FLOW > 150 kg/h                         |
| EFF-1 | HIGH O2 OVER TEMPERATURE | TRIPS W                                 |
| EFF-2 |                          | TRIP / MAINTAIN / INCREASE FLOW ON TRIP |
| EFF-3 |                          | FLOW ON TRIP                            |
| P1-P4 | PERMISSIVE TO            | ENABLE STARTUP                          |


## Notes
1. COORDINATE IN PLANT DWG USING METRES.
2. ELEVATIONS RELATIVE TO CHASE EL V1-40
3. EQUIPMENT SHOWN AT APPROX FOOTPRINT SCALE.
4. HAZARDOUS AREA CLASSIFICATION FOR mss MAT OLL.
