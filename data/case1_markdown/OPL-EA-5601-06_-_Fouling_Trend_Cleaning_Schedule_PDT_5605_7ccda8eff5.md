<!-- case1_doc_name: OPL-EA-5601-06 - Fouling_Trend_Cleaning_Schedule_PDT_5605.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                       | OPL No: **OPL-EA-5601-06**<br/>Sheet 1 of 1 |                               |                               |
| ------------------------------------------------------ | ------------------------------------------------ | ------------------------------------------- | ----------------------------- | ----------------------------- |
| **OPL Title**                                          | **Fouling Trend & Cleaning Schedule (PDT-5605)** | **Discipline**                              | Instrument                    |                               |
| **Equipment**                                          | EA-5601 - SOLVENT HEATER                         | **Area / Unit**                             | 5600 - SOLVENT HEATING SYSTEM |                               |
| **Related Interlock**                                  | N/A (control loop only) (N/A)                    | **P\&ID Ref**                               | TJC-LLD-PID-5601              |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                             | \[X] Improvement                            | \[ ] Trouble Case             | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **fouling trend & cleaning schedule (pdt-5605)** for EA-5601 (SOLVENT HEATER) in the SOLVENT HEATING SYSTEM. Trending the tube-side differential pressure predicts when cleaning is due before the duty is lost. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **LOW CRITICAL** handling **Hexane / MP Steam** at up to 16 barg (tube) / 200 degC. Observe the following before and during the task:

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

| Step | Action                                                    | Check / Acceptance             |
| ---- | --------------------------------------------------------- | ------------------------------ |
| 1    | Log PDT-5605 differential pressure weekly                 | Loop isolated / under permit   |
| 2    | Note the PDAH-5605 fouling alarm at 0.7 bar dP            | Reference standard traceable   |
| 3    | Correlate rising dP with any outlet-temperature shortfall | As-found & as-left recorded    |
| 4    | Plan cleaning before the duty loss becomes critical       | Trip / control action verified |
| 5    | Feed the trend into the exchanger cleaning program        | Return to service confirmed    |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Outlet temperature hunting around set-point</td>
<td>Steam valve TV-5602 loop poorly tuned</td>
<td>Retuned TIC-5602 PID, verified stable control</td>
  </tr>
<tr>
    <td>Erratic tube dP reading</td>
<td>Impulse lines plugged with fines</td>
<td>Cleaned and re-zeroed PDT-5605 transmitter</td>
  </tr>
<tr>
    <td>Cracked gauge glass on condensate pot</td>
<td>Thermal/mechanical stress on glass</td>
<td>Replaced LG-5606 gauge glass and seals</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- Trending the tube-side differential pressure predicts when cleaning is due before the duty is lost.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-5601 before working on EA-5601.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing     |
| --------------------------- | ------------------------ | ------------------------ | ------------------- |
| Panel Operator / Technician | Yudha Permana (EMP-1124) | Arya Wibisono (EMP-0912) | Monday, 25 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
