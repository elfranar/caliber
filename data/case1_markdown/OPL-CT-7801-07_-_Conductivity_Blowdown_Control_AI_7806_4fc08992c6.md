<!-- case1_doc_name: OPL-CT-7801-07 - Conductivity_Blowdown_Control_AI_7806.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                    | OPL No: **OPL-CT-7801-07**<br/>Sheet 1 of 1 |                             |                               |
| ------------------------------------------------------ | --------------------------------------------- | ------------------------------------------- | --------------------------- | ----------------------------- |
| **OPL Title**                                          | **Conductivity / Blowdown Control (AI-7806)** | **Discipline**                              | Process / Operations        |                               |
| **Equipment**                                          | CT-7801 - COOLING TOWER CELL FAN              | **Area / Unit**                             | 7800 - COOLING TOWER SYSTEM |                               |
| **Related Interlock**                                  | SEQ-7801 (SIL 1)                              | **P\&ID; Ref**                              | TJC-LLD-PID-7801            |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                          | \[X] Improvement                            | \[ ] Trouble Case           | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **conductivity / blowdown control (ai-7806)** for CT-7801 (COOLING TOWER CELL FAN) in the COOLING TOWER SYSTEM. High conductivity means the water is over-concentrated; automatic blowdown keeps the cycles of concentration in range. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **NON CRITICAL** handling **Circulating water / air** at up to atm / 50 degC. Observe the following before and during the task:

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

| Step | Action                                               | Check / Acceptance         |
| ---- | ---------------------------------------------------- | -------------------------- |
| 1    | Read the AI-7806 conductivity value                  | Permit valid & briefed     |
| 2    | Verify the automatic blowdown valve XV-7806 operates | Parameter within limit     |
| 3    | Maintain the target cycles of concentration          | Interlock status confirmed |
| 4    | Log make-up versus blowdown volumes                  | Change logged on DCS       |
| 5    | Coordinate chemical dosing with water treatment      | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Routine barscreen cleaning on operator round</td>
<td>Normal debris accumulation</td>
<td>Raked barscreen clear, checked differential level</td>
  </tr>
<tr>
    <td>Scheduled fan gearbox oil change</td>
<td>Routine - oil sample acceptable</td>
<td>Drained and refilled ISO VG 220, replaced breather</td>
  </tr>
<tr>
    <td>VSHH-7802 vibration alarm on CT-7801 fan</td>
<td>Leading-edge erosion on one FRP blade caused imbalance</td>
<td>Inspected blades, re-balanced fan, vibration normalised</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- High conductivity means the water is over-concentrated; automatic blowdown keeps the cycles of concentration in range.
- Respect the interlock SEQ-7801: e.g. VSHH-7802 trips at > 9 mm/s - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-7801 before working on CT-7801.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing        |
| --------------------------- | ------------------------ | ------------------------ | ---------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Arya Wibisono (EMP-0912) | Saturday, 20 June 2026 |


Cross-ref tag CT-7801 across Datasheet, GA, P&ID, Interlock and Maintenance History
