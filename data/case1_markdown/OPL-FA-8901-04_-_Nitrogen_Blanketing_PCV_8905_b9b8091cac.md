<!-- case1_doc_name: OPL-FA-8901-04 - Nitrogen_Blanketing_PCV_8905.pdf | case1_version: iewed -->

| **This is sample data provided**<br/>for CALIBER purposes only | **ONE POINT LESSON (OPL)**         | OPL No: **OPL-FA-8901-04**<br/>Sheet 1 of 1 |                                      |                               |
| -------------------------------------------------------------- | ---------------------------------- | ------------------------------------------- | ------------------------------------ | ----------------------------- |
| **OPL Title**                                                  | **Nitrogen Blanketing (PCV-8905)** | **Discipline**                              | Process / Operations                 |                               |
| **Equipment**                                                  | FA-8901 - REFLUX ACCUMULATOR DRUM  | **Area / Unit**                             | 8900 - HEXANE COLUMN OVERHEAD SYSTEM |                               |
| **Related Interlock**                                          | SEQ-8901 (SIL 1)                   | **P\&ID; Ref**                              | TJC-LLD-PID-8901                     |                               |
| **Classification:**                                            | \[X] Basic Knowledge               | \[ ] Improvement                            | \[ ] Trouble Case                    | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **nitrogen blanketing** (**pcv-8905**) for FA-8901 (REFLUX ACCUMULATOR DRUM) in the HEXANE COLUMN OVERHEAD SYSTEM. The nitrogen blanket keeps air out of the hexane drum and holds a stable pressure; loss of blanket risks an explosive atmosphere. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **Hexane / water** at up to 10 barg / FV / 120 degC. Observe the following before and during the task:

- Obtain the correct operating permit and brief the shift team before the task.
- Confirm hazardous fluids are isolated / inerted as required by procedure.
- Beware of flammable, hot, or high-pressure fluids; wear the correct PPE.
- Never defeat a safety interlock or trip without an authorised override permit.
- Have emergency actions and communications ready before starting.

## 3. TOOLS & MATERIALS REQUIRED

- Operating procedure & P&ID;
- Radio / communication with panel
- Gas detector (O2 / LEL) as required
- Correct PPE for the fluid handled
- Sample containers & PPE for sampling
- Permit-to-work documentation

## 4. DETAILED PROCEDURE / STEPS

| Step | Action                                                 | Check / Acceptance         |
| ---- | ------------------------------------------------------ | -------------------------- |
| 1    | Verify the PCV-8905 split-range holds PT-8902 pressure | Permit valid & briefed     |
| 2    | Confirm the blanket makes up on falling pressure       | Parameter within limit     |
| 3    | Confirm the vent relieves on rising pressure           | Interlock status confirmed |
| 4    | Respond immediately to a blanket-loss alarm            | Change logged on DCS       |
| 5    | Check the N2 supply header pressure is adequate        | Handover to next shift     |


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
    <td>Statutory relief valve test</td>
<td>Set pressure drift found</td>
<td>Overhauled PSV-8901, lapped seat, re-set 10 barg, certified</td>
  </tr>
<tr>
    <td>Boot drain valve N4 passing / leaking</td>
<td>Seat eroded by water/solids</td>
<td>Reseated / replaced boot drain valve HV-8904</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- The nitrogen blanket keeps air out of the hexane drum and holds a stable pressure; loss of blanket risks an explosive atmosphere.
- Respect the interlock SEQ-8901: e.g. LSHH-8901 trips at > 85 % - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-8901 before working on FA-8901.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)       | Date of Sharing      |
| --------------------------- | ------------------------ | --------------------------- | -------------------- |
| Panel Operator / Technician | Yudha Permana (EMP-1124) | Zulkarnain Hasan (EMP-0901) | Friday, 19 June 2026 |


Cross-ref tag FA-8901 across Datasheet, GA, P&ID, Interlock and Maintenance History.
