<!-- case1_doc_name: OPL-FA-8901-01 - Level_Gauge_Bridle_Verification_LT_8901.pdf | case1_version: iewed -->

| **This is sample data provided**<br/>for CALIBER purposes only | **ONE POINT LESSON (OPL)**                  | OPL No: **OPL-FA-8901-01**<br/>Sheet 1 of 1 |                                      |                               |
| -------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------ | ----------------------------- |
| **OPL Title**                                                  | Level Gauge / Bridle Verification (LT-8901) | **Discipline**                              | Instrument                           |                               |
| **Equipment**                                                  | FA-8901 - REFLUX ACCUMULATOR DRUM           | **Area / Unit**                             | 8900 - HEXANE COLUMN OVERHEAD SYSTEM |                               |
| **Related Interlock**                                          | SEQ-8901 (SIL 1)                            | **P\&ID; Ref**                              | TJC-LLD-PID-8901                     |                               |
| **Classification:**                                            | \[X] Basic Knowledge                        | \[ ] Improvement                            | \[ ] Trouble Case                    | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **level gauge / bridle verification (Lt-8901)** for FA-8901 (REFLUX ACCUMULATOR DRUM) in the HEXANE COLUMN OVERHEAD SYSTEM. A false level reading causes reflux pump cavitation (low) or column flooding (high); the transmitter must agree with the gauge. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **Hexane / water** at up to 10 barg / FV / 120 degC. Observe the following before and during the task:

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

| Step | Action                                                   | Check / Acceptance             |
| ---- | -------------------------------------------------------- | ------------------------------ |
| 1    | Cross-check LT-8901 against the level bridle gauge       | Loop isolated / under permit   |
| 2    | Blow down the bridle to clear any plugging               | Reference standard traceable   |
| 3    | Confirm the LSHH-8901 and LSLL-8901 switch actions       | As-found & as-left recorded    |
| 4    | Verify the level tracks correctly through a level change | Trip / control action verified |
| 5    | Log any deviation and recalibrate if needed              | Return to service confirmed    |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Reflux drum level transmitter drifting vs gauge</td>
<td>Transmitter zero drift</td>
<td>Recalibrated LT-8901 against the bridle gauge</td>
  </tr>
<tr>
    <td>Blanket / vent split-range valve hunting</td>
<td>Split-range calibration overlap incorrect</td>
<td>Re-tuned PCV-8905 split-range, verified PT-8902 hold</td>
  </tr>
<tr>
    <td>Proof test of drum high-high level trip</td>
<td>Within tolerance</td>
<td>Recalibrated LSHH-8901 and verified EFF-1 column feed trip</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- A false level reading causes reflux pump cavitation (low) or column flooding (high); the transmitter must agree with the gauge.
- Respect the interlock SEQ-8901: e.g. LSHH-8901 trips at > 85 % - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-8901 before working on FA-8901.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)       | Date of Sharing      |
| --------------------------- | ------------------------ | --------------------------- | -------------------- |
| Panel Operator / Technician | Yudha Permana (EMP-1124) | Zulkarnain Hasan (EMP-0901) | Sunday, 07 June 2026 |


Cross-ref tag FA-8901 across Datasheet, GA, P&ID, Interlock and Maintenance History.
