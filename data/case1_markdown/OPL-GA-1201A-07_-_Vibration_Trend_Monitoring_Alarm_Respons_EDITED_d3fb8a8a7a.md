<!-- case1_doc_name: OPL-GA-1201A-07 - Vibration_Trend_Monitoring_Alarm_Respons_EDITED.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                                  | OPL No: **OPL-GA-1201A-07**<br/>Sheet 1 of 1 |                           |                               |
| ------------------------------------------------------ | ----------------------------------------------------------- | -------------------------------------------- | ------------------------- | ----------------------------- |
| **OPL Title**                                          | **Vibration Trend Monitoring & Alarm Response (VSHH-1201)** | **Discipline**                               | Instrument                |                               |
| **Equipment**                                          | GA-1201A - HEXANE FEED PUMP                                 | **Area / Unit**                              | 1200 - HEXANE FEED SYSTEM |                               |
| **Related Interlock**                                  | SEQ-1201 (SIL 1)                                            | **P\&ID; Ref**                               | TJC-LLD-PID-1201          |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                                        | \[X] Improvement                             | \[ ] Trouble Case         | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **vibration trend monitoring & alarm response (vshh-1201)** for GA-1201A (HEXANE FEED PUMP) in the HEXANE FEED SYSTEM. A rising vibration trend predicts bearing failure days in advance and lets you plan a repair before a trip. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **n-Hexane** at up to 16 barg / 80 degC. Observe the following before and during the task:

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

| Step | Action                                                                       | Check / Acceptance             |
| ---- | ---------------------------------------------------------------------------- | ------------------------------ |
| 1    | Record VT-1201 on the daily PdM route in mm/s RMS                            | Loop isolated / under permit   |
| 2    | Note alarm at 4.5 mm/s and trip at 7.1 mm/s (VSHH-1201)                      | Reference standard traceable   |
| 3    | A rise greater than 1 mm/s within a week = plan a bearing inspection         | As-found & as-left recorded    |
| 4    | Correlate the vibration rise with TI-1201 bearing temperature                | Trip / control action verified |
| 5    | Escalate to reliability engineer if the 1x running-speed component dominates | Return to service confirmed    |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Scheduled proof test of low-low suction pressure trip</td>
<td>Switch set-point drift found +0.08 barg during proof test</td>
<td>Recalibrated PSLL-1201 to 0.5 barg trip, function tested to DCS</td>
  </tr>
<tr>
    <td>PDI-1201 reading erratic, seal-flush low alarm nuisance-tripping</td>
<td>Impulse lines fouled with hexane residue/polymer fines</td>
<td>Cleaned impulse lines and re-zeroed PDI-1201 transmitter</td>
  </tr>
<tr>
    <td>Discharge flow control hunting, FIC-1201 oscillating</td>
<td>Loop poorly tuned after transmitter re-range</td>
<td>Re-ranged FT-1201 and retuned FIC-1201 PID parameters</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- A rising vibration trend predicts bearing failure days in advance and lets you plan a repair before a trip.
- Respect the interlock SEQ-1201: e.g. PSLL-1201 trips at < 0.5 barg - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-1201 before working on GA-1201A.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing          |
| --------------------------- | ------------------------ | ------------------------ | ------------------------ |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Arya Wibisono (EMP-0912) | Wednesday, 15 April 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID; Interlock and Maintenance History
