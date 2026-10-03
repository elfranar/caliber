<!-- case1_doc_name: OPL-CT-7801-04 - Circulating_Water_pH_Control_AI_7805.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                 | OPL No: **OPL-CT-7801-04**<br/>Sheet 1 of 1 |                             |                               |
| ------------------------------------------------------ | ------------------------------------------ | ------------------------------------------- | --------------------------- | ----------------------------- |
| **OPL Title**                                          | **Circulating Water pH Control (AI-7805)** | **Discipline**                              | Process / Operations        |                               |
| **Equipment**                                          | CT-7801 - COOLING TOWER CELL FAN           | **Area / Unit**                             | 7800 - COOLING TOWER SYSTEM |                               |
| **Related Interlock**                                  | SEQ-7801 (SIL 1)                           | **P\&ID; Ref**                              | TJC-LLD-PID-7801            |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                       | \[X] Improvement                            | \[ ] Trouble Case           | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **circulating water ph control (ai-7805)** for CT-7801 (COOLING TOWER CELL FAN) in the COOLING TOWER SYSTEM. Wrong pH causes scaling or corrosion across the entire cooling water loop, not just this cell. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

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

| Step | Action                                            | Check / Acceptance         |
| ---- | ------------------------------------------------- | -------------------------- |
| 1    | Read the AI-7805 pH each shift (target 7.0-8.5)   | Permit valid & briefed     |
| 2    | Check the acid / caustic dosing pumps are running | Parameter within limit     |
| 3    | Cross-check against a manual lab titration        | Interlock status confirmed |
| 4    | Adjust the dosing set-point as needed             | Change logged on DCS       |
| 5    | Report large pH swings to water treatment         | Handover to next shift     |


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

- Wrong pH causes scaling or corrosion across the entire cooling water loop, not just this cell.
- Respect the interlock SEQ-7801: e.g. VSHH-7802 trips at > 9 mm/s - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-7801 before working on CT-7801.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing      |
| --------------------------- | ------------------------ | ------------------------ | -------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Arya Wibisono (EMP-0912) | Monday, 08 June 2026 |


Cross-ref tag CT-7801 across Datasheet, GA, P&ID, Interlock and Maintenance History
