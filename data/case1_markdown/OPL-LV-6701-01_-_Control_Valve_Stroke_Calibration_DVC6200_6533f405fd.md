<!-- case1_doc_name: OPL-LV-6701-01 - Control_Valve_Stroke_Calibration_DVC6200.pdf | case1_version: iewed -->

This is sample data provided for CALIBER purposes only
# ONE POINT LESSON (OPL)
OPL No: **OPL-LV-6701-01**
Sheet 1 of 1

| **OPL Title**         | **Control Valve Stroke Calibration (DVC6200)** | **Discipline**   | Instrument                 |                               |
| --------------------- | ---------------------------------------------- | ---------------- | -------------------------- | ----------------------------- |
| **Equipment**         | LV-6701 - SEPARATOR LEVEL CONTROL VALVE        | **Area / Unit**  | 6700 - LP SEPARATOR SYSTEM |                               |
| **Related Interlock** | SEQ-6701 (SIL 1)                               | **P\&ID Ref**    | TJC-LLD-PID-6701           |                               |
| **Classification:**   | \[X] Basic Knowledge                           | \[ ] Improvement | \[ ] Trouble Case          | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **control valve stroke calibration (dvc6200)** for LV-6701 (SEPARATOR LEVEL CONTROL VALVE) in the LP SEPARATOR SYSTEM. Correct mapping of the 4-20 mA signal to 0-100 % valve stroke is essential for stable separator level control. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **LOW CRITICAL** handling **Hexane + polymer bottoms** at up to ASME 300# / 120 degC. Observe the following before and during the task:

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

| Step | Action                                            | Check / Acceptance             |
| ---- | ------------------------------------------------- | ------------------------------ |
| 1    | Connect ValveLink to the DVC6200 positioner       | Loop isolated / under permit   |
| 2    | Run the auto-calibration over the full stroke     | Reference standard traceable   |
| 3    | Verify 4 mA = closed and 20 mA = 38 mm fully open | As-found & as-left recorded    |
| 4    | Check hysteresis and dead-band are within 1 %     | Trip / control action verified |
| 5    | Save the calibration and record the as-left data  | Return to service confirmed    |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>LV-6701 not responding to LIC-6701, level control lost</td>
<td>Stem seized in PTFE packing (over-tightened + fines)</td>
<td>Freed stem, renewed packing, lubricated, re-stroked and calibrated</td>
  </tr>
<tr>
    <td>Positioner giving position error after drift</td>
<td>Positioner feedback out of calibration</td>
<td>Recalibrated DVC6200, updated firmware, verified travel</td>
  </tr>
<tr>
    <td>Hexane weeping at LV-6701 stem packing</td>
<td>PTFE V-ring packing worn</td>
<td>Renewed PTFE V-ring packing set, re-torqued gland</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- Correct mapping of the 4-20 mA signal to 0-100 % valve stroke is essential for stable separator level control.
- Respect the interlock SEQ-6701: e.g. LSHH-6710 trips at > 85 % - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-6701 before working on LV-6701.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor)   | Approved by (Manager)       | Date of Sharing       |
| --------------------------- | -------------------------- | --------------------------- | --------------------- |
| Panel Operator / Technician | Vino Ardiansyah (EMP-1102) | Zulkarnain Hasan (EMP-0901) | Saturday, 16 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
