<!-- case1_doc_name: OPL-DC-3401A-06 Multipoint_Thermocouple_TE_3401_Verifica.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                       | OPL No: **OPL-DC-3401A-06**<br/>Sheet 1 of 1 |                                  |                               |
| ------------------------------------------------------ | ------------------------------------------------ | -------------------------------------------- | -------------------------------- | ----------------------------- |
| **OPL Title**                                          | **Multipoint Thermocouple TE-3401 Verification** | **Discipline**                               | Instrument                       |                               |
| **Equipment**                                          | DC-3401A - CATALYST REDUCTION REACTOR            | **Area / Unit**                              | 3400 - CATALYST REDUCTION SYSTEM |                               |
| **Related Interlock**                                  | SEQ-3401 (SIL 2)                                 | **P\&ID Ref**                                | TJC-LLD-PID-3401                 |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                             | \[X] Improvement                             | \[ ] Trouble Case                | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **multipoint thermocouple te-3401 verification** for DC-3401A (CATALYST REDUCTION REACTOR) in the CATALYST REDUCTION SYSTEM. The 8-point bed temperature profile drives the whole reduction; a failed or drifting thermocouple can hide a hot spot. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **N2 / H2 / Pd catalyst** at up to 6 barg / FV / 250 degC. Observe the following before and during the task:

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

| Step | Action                                                             | Check / Acceptance             |
| ---- | ------------------------------------------------------------------ | ------------------------------ |
| 1    | Verify all 8 TE-3401 points are reading and note the spread        | Loop isolated / under permit   |
| 2    | Flag any single TC more than 15 degC off its neighbours            | Reference standard traceable   |
| 3    | Cross-check the profile against TIC-17343 heater outlet            | As-found & as-left recorded    |
| 4    | Replace any open-circuit or drifting TC at the next opportunity    | Trip / control action verified |
| 5    | Confirm TSHH-3401 selects the highest bed temperature for the trip | Return to service confirmed    |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Bed multipoint TC point 3 reading open circuit</td>
<td>Thermocouple element failed at the sheath junction</td>
<td>Replaced TC point 3 in the multipoint assembly, verified reading.</td>
  </tr>
<tr>
    <td>Inerting O2 analyzer drift vs portable reference</td>
<td>Analyzer zero drift and sample dryer saturated</td>
<td>Recalibrated AI-3401 on span gas, replaced sample dryer</td>
  </tr>
<tr>
    <td>N2 inert valve slow / sticking during inerting step</td>
<td>Actuator seals hardened, positioner out of calibration</td>
<td>Serviced actuator, replaced seals, recalibrated positioner</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- The 8-point bed temperature profile drives the whole reduction; a failed or drifting thermocouple can hide a hot spot.
- Respect the interlock SEQ-3401: e.g. TSHH-3401 trips at > 230 degC - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-3401 before working on DC-3401A.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor)   | Approved by (Manager)    | Date of Sharing     |
| --------------------------- | -------------------------- | ------------------------ | ------------------- |
| Panel Operator / Technician | Vino Ardiansyah (EMP-1102) | Arya Wibisono (EMP-0912) | Sunday, 03 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
