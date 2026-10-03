<!-- case1_doc_name: P&ID_Set 7.png | case1_version: Not specified -->

# P&ID: COOLING TOWER FAN (CT-7801) SYSTEM

**CT-7801** Composite Drive Shaft Arrangement

**CT-7801**
55 kW, TEFC IP56
Area Non-hazardous
Voltage 380 V/3 Ph/50 Hz ( per image_0.png)

**VSIFH-7802** Axial induced draft fan 6 FRP blades (as in <IMAGE 1>)

**FI 1201**

**PT-1201**

**PSLL 1201**

**VENT**

**COOLING TOWER CELL**

**VENT**

**COOLING TOWER**

**Drainess Drain**

**DRAIN**

**Basin Drain**

| INTERLOCK SEQ-7801<br/>IDLimiterFan vibration<br/>Fan vibration<br/>Gearbox oil temp<br/>Gearbox oil pressure<br/>Fan motor overload                                                                                           | INTERLOCK SEQ-7801<br/>TagVSHH-7802<br/>VSHH-7802<br/>TSHH-7802<br/>PSL-7807<br/>MPR-7801 | INTERLOCK SEQ-7801<br/>test/ act.>9 mm/s<br/>=90 dag C<br/>=90 dag C<br/>0.8 barg<br/>MPR pickup | INTERLOCK SEQ-7801<br/>Effects<br/>EFF-1<br/>1<br/>1<br/>1<br/>1<br/>1 | INTERLOCK SEQ-7801<br/>Effects<br/>EFF-2<br/>✷<br/>XX | INTERLOCK SEQ-7801<br/>Effects<br/>EFF-3<br/>T1<br/>X<br/>X<br/>X | INTERLOCK SEQ-7801<br/>EffectsT2<br/>X<br/>X | Final Element / Action<br/>T3X | T4 | Trip Fan Motor CT-7801<br/>Trip Fan Motor CT-7801<br/>Annunciate Alarm on DCS<br/>Request Start of Spare Coil CT-7802<br/>Request Start of Spare Coil CT-7802<br/>→ Spare Coil P\&ID |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------- | ------------------------------ | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **START PERMISSIVE (AND-gate)**                                                                                                                                                                                                |                                                                                           |                                                                                                  |                                                                        |                                                       |                                                                   |                                              |                                |    |                                                                                                                                                                                      |
| - LG Gearbox oil level OK<br/>- LT-7804 Basin level normal<br/>Basin level normal (LSL-7804)<br/>- lockout release logic<br/>- L Gearbox oil level OK < Other (LSL-7804)<br/>- Lockout release logic in orlft per image\_0.png |                                                                                           |                                                                                                  |                                                                        |                                                       |                                                                   |                                              |                                |    |                                                                                                                                                                                      |


**LEGEND**
- ○ LOGIC hum/
- ⤓ START PERMISSIVE
- ⨌ TRIP
- ⨁ CAUSE EFFECT

Ref. Plog. TJC-LLD-PID-XXXX

**NOTES:**
NOTE 1. This is sample data provided for CALIBER purpose only;
NOTE 2: Refer to Datasheet TJC-LLD-DS-GA-7801A for design parameters;
NOTE 3: See SEQ-7801 logic diagram.
