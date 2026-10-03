<!-- case1_doc_name: OPL-CT-7801-06 - Gearbox_Vibration_Monitoring_VSHH_7802.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                   | OPL No: **OPL-CT-7801-06**<br/>Sheet 1 of 1 |                             |                               |
| ------------------------------------------------------ | -------------------------------------------- | ------------------------------------------- | --------------------------- | ----------------------------- |
| **OPL Title**                                          | **Gearbox Vibration Monitoring (VSHH-7802)** | **Discipline**                              | Instrument                  |                               |
| **Equipment**                                          | CT-7801 - COOLING TOWER CELL FAN             | **Area / Unit**                             | 7800 - COOLING TOWER SYSTEM |                               |
| **Related Interlock**                                  | SEQ-7801 (SIL 1)                             | **P\&ID; Ref**                              | TJC-LLD-PID-7801            |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                         | \[X] Improvement                            | \[ ] Trouble Case           | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **gearbox vibration monitoring (vshh-7802)** for CT-7801 (COOLING TOWER CELL FAN) in the COOLING TOWER SYSTEM. A rising vibration trend warns of gear or bearing wear before the fan trips or throws a blade. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **NON CRITICAL** handling **Circulating water / air** at up to atm / 50 degC. Observe the following before and during the task:

- De-energise and isolate the loop; place the function to bypass/inhibit under permit.
- Inform the panel operator before working on any trip, valve or transmitter.
- Take care with instrument air / hydraulic pressure when disconnecting tubing.
- Verify intrinsic-safety / Ex integrity is restored before returning to service.
- Wear correct PPE and follow ESD/override control procedures.

## 3. TOOLS & MATERIALS REQUIRED

- HART communicator / positioner software (e.g. ValveLink)
- Loop calibrator & decade box / pressure source
- Digital multimeter and clamp meter
- Span/zero test gas or reference standards
- Torque screwdriver and small hand tools
- Certified test/inhibit permit

## 4. DETAILED PROCEDURE / STEPS

| Step | Action                                                  | Check / Acceptance             |
| ---- | ------------------------------------------------------- | ------------------------------ |
| 1    | Trend the VS-7802 reading on the PdM route              | Loop isolated / under permit   |
| 2    | Alarm at 6 mm/s and trip at 9 mm/s (VSHH-7802)          | Reference standard traceable   |
| 3    | Correlate the rise with gearbox oil temperature TE-7803 | As-found & as-left recorded    |
| 4    | Inspect the floating drive-shaft couplings              | Trip / control action verified |
| 5    | Escalate a step-change to reliability                   | Return to service confirmed    |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Scheduled pH analyzer calibration</td>
<td>Electrode drift</td>
<td>Recalibrated AI-7805 on buffer solutions, replaced electrode</td>
  </tr>
<tr>
    <td>Blowdown conductivity reading unreliable</td>
<td>Conductivity cell fouled with scale</td>
<td>Cleaned and recalibrated AI-7806 conductivity cell</td>
  </tr>
<tr>
    <td>Routine barscreen cleaning on operator round</td>
<td>Normal debris accumulation</td>
<td>Raked barscreen clear, checked differential level</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- A rising vibration trend warns of gear or bearing wear before the fan trips or throws a blade.
- Respect the interlock SEQ-7801: e.g. VSHH-7802 trips at > 9 mm/s - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-7801 before working on CT-7801.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing       |
| --------------------------- | ------------------------ | ------------------------ | --------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Arya Wibisono (EMP-0912) | Tuesday, 16 June 2026 |


Cross-ref tag CT-7801 across Datasheet, GA, P&ID, Interlock and Maintenance History
