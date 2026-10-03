<!-- case1_doc_name: OPL-KC-4501-05 Crosshead_Vibration_Monitoring_VSHH_4505.pdf | case1_version: ersals -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                     | OPL No: **OPL-KC-4501-05**<br/>Sheet 1 of 1 |                           |                               |
| ------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------- | ----------------------------- |
| **OPL Title**                                          | **Crosshead Vibration Monitoring (VSHH-4505)** | **Discipline**                              | Instrument                |                               |
| **Equipment**                                          | KC-4501 - RECYCLE GAS COMPRESSOR               | **Area / Unit**                             | 4500 - RECYCLE GAS SYSTEM |                               |
| **Related Interlock**                                  | SEQ-4501 (SIL 2)                               | **P\&ID Ref**                               | TJC-LLD-PID-4501          |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                           | \[X] Improvement                            | \[ ] Trouble Case         | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **crosshead vibration monitoring** (**vshh-4505**) for KC-4501 (RECYCLE GAS COMPRESSOR) in the RECYCLE GAS SYSTEM. A rising crosshead vibration trend warns of loose running gear before it trips or fails. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **Ethylene/Hexane/H2** at up to 16 barg / 150 degC. Observe the following before and during the task:

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

| Step | Action                                                     | Check / Acceptance             |
| ---- | ---------------------------------------------------------- | ------------------------------ |
| 1    | Trend VT-4501 crosshead vibration on the daily route       | Loop isolated / under permit   |
| 2    | Alarm at 8 mm/s and trip at 11 mm/s (VSHH-4505)            | Reference standard traceable   |
| 3    | Correlate any rise with TE-4507 main bearing temperature   | As-found & as-left recorded    |
| 4    | Investigate rod-load reversals and crosshead pin clearance | Trip / control action verified |
| 5    | Escalate a sudden step-change to reliability immediately   | Return to service confirmed    |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Proof test of lube oil low-low trip</td>
<td>Set-point within tolerance</td>
<td>Recalibrated PSLL-4504 to 1.5 barg, function tested</td>
  </tr>
<tr>
    <td>Seal gas flow FT-4506 low, buffer pressure unstable</td>
<td>N2 buffer regulator diaphragm failed</td>
<td>Replaced seal gas regulator, re-established buffer dP</td>
  </tr>
<tr>
    <td>Proof test of KO drum high-high level trip</td>
<td>Float healthy, minor set-point trim</td>
<td>Verified LSHH-4510 float and trip action</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- A rising crosshead vibration trend warns of loose running gear before it trips or fails.
- Respect the interlock SEQ-4501: e.g. PSLL-4504 trips at < 1.5 barg - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-4501 before working on KC-4501.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)       | Date of Sharing     |
| --------------------------- | ------------------------ | --------------------------- | ------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Zulkarnain Hasan (EMP-0901) | Sunday, 10 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
