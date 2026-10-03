<!-- case1_doc_name: OPL-EA-5601-03 - Steam_Trap_Health_Check.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**    | OPL No: **OPL-EA-5601-03**<br/>Sheet 1 of 1 |                               |                               |
| ------------------------------------------------------ | ----------------------------- | ------------------------------------------- | ----------------------------- | ----------------------------- |
| **OPL Title**                                          | **Steam Trap Health Check**   | **Discipline**                              | Process / Operations          |                               |
| **Equipment**                                          | EA-5601 - SOLVENT HEATER      | **Area / Unit**                             | 5600 - SOLVENT HEATING SYSTEM |                               |
| **Related Interlock**                                  | N/A (control loop only) (N/A) | **P\&ID Ref**                               | TJC-LLD-PID-5601              |                               |
| **Classification:**                                    | \[ ] Basic Knowledge          | \[X] Improvement                            | \[ ] Trouble Case             | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **steam trap health check** for EA-5601 (SOLVENT HEATER) in the SOLVENT HEATING SYSTEM. A failed steam trap either floods the shell (killing duty) or blows live steam (wasting energy); regular checks catch both. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **LOW CRITICAL** handling **Hexane / MP Steam** at up to 16 barg (tube) / 200 degC. Observe the following before and during the task:

- Obtain the correct operating permit and brief the shift team before the task.
- Confirm hazardous fluids are isolated / inerted as required by procedure.
- Beware of flammable, hot, or high-pressure fluids; wear the correct PPE.
- Never defeat a safety interlock or trip without an authorised override permit.
- Have emergency actions and communications ready before starting.

## 3. TOOLS & MATERIALS REQUIRED

- Operating procedure & P&ID
- Radio / communication with panel
- Gas detector (O2 / LEL) as required
- Correct PPE for the fluid handled
- Sample containers & PPE for sampling
- Permit-to-work documentation

## 4. DETAILED PROCEDURE / STEPS

| Step | Action                                                                 | Check / Acceptance         |
| ---- | ---------------------------------------------------------------------- | -------------------------- |
| 1    | Compare the condensate temperature TI-5604 to steam temperature        | Permit valid & briefed     |
| 2    | Use ultrasonic or a listening stick to check trap operation            | Parameter within limit     |
| 3    | A cold trap means flooding; a continuously hot blow means leak-through | Interlock status confirmed |
| 4    | Check the condensate pot level gauge LG-5606                           | Change logged on DCS       |
| 5    | Replace the trap element or trap as required                           | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>High tube dP PDT-5605, low solvent outlet temperature</td>
<td>Hexane fouling / polymer fines deposit on tube bores</td>
<td>Hydrojetted 246 tubes, restored dP and duty, re-gasketed</td>
  </tr>
<tr>
    <td>Hexane weep at channel flange</td>
<td>Spiral-wound channel gasket relaxed / damaged</td>
<td>Renewed channel gasket, re-torqued in cross pattern</td>
  </tr>
<tr>
    <td>Continuous steam at condensate, high steam use</td>
<td>Steam trap element failed open</td>
<td>Replaced steam trap element, verified condensate temperature</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- A failed steam trap either floods the shell (killing duty) or blows live steam (wasting energy); regular checks catch both.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-5601 before working on EA-5601.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing        |
| --------------------------- | ------------------------ | ------------------------ | ---------------------- |
| Panel Operator / Technician | Yudha Permana (EMP-1124) | Arya Wibisono (EMP-0912) | Wednesday, 13 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
