<!-- case1_doc_name: OPL-GA-1201A-04 - Minimum_Flow_Line_Operation_Deadhead_Pro_EDITED_KEEP_SIZE_REFINED_TABLE.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                            | OPL No: **OPL-GA-1201A-04**<br/>Sheet 1 of 1 |                           |                           |
| ------------------------------------------------------ | ----------------------------------------------------- | -------------------------------------------- | ------------------------- | ------------------------- |
| **OPL Title**                                          | **Minimum Flow Line Operation & Deadhead Protection** | **Discipline**                               | Process / Operations      |                           |
| **Equipment**                                          | GA-1201A - HEXANE FEED PUMP                           | **Area / Unit**                              | 1200 - HEXANE FEED SYSTEM |                           |
| **Related Interlock**                                  | SEQ-1201 (SIL 1)                                      | **P\&ID; Ref**                               | TJC-LLD-PID-1201          |                           |
| **Classification:**                                    | \[X] Basic Knowledge                                  | \[ ] Improvement                             | \[ ] Trouble Case         | Aspect: P-Q-C-D-**S**-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **minimum flow line operation & deadhead protection** for GA-1201A (HEXANE FEED PUMP) in the HEXANE FEED SYSTEM. Never run the pump against a closed discharge. The min-flow recycle (FV-1201) protects the pump from deadhead overheating. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **n-Hexane** at up to 16 barg / 80 degC. Observe the following before and during the task:

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

| Step | Action                                                                           | Check / Acceptance         |
| ---- | -------------------------------------------------------------------------------- | -------------------------- |
| 1    | Confirm FV-1201 min-flow recycle line is open before start                       | Permit valid & briefed     |
| 2    | Watch that FIC-1201 stays above the 9 m3/h minimum continuous flow               | Parameter within limit     |
| 3    | If FSLL-1201 trips, check downstream XV-1201 and manual valves for a closed path | Interlock status confirmed |
| 4    | Do not defeat the min-flow interlock to force higher discharge pressure          | Change logged on DCS       |
| 5    | Reset the pump only after the low-flow cause has been cleared                    | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Hexane leak observed at GA-1201A seal gland during operation, seal dr</td>
<td>API Plan 11 flush orifice RO-1201 partially plugged causing seal face</td>
<td>Replaced JC T2100 mechanical seal cartridge, cleaned flush orifice, v</td>
  </tr>
<tr>
    <td>GA-1201A tripped on VSHH-1201 high vibration 7.4 mm/s</td>
<td>Angular misalignment 0.12 mm/100mm after foundation settlement</td>
<td>Laser re-aligned pump/motor, re-shimmed motor feet, vibration back to</td>
  </tr>
<tr>
    <td>Bearing DE noisy with rising temperature TI-1201 trend</td>
<td>Outer race spalling on DE bearing due to prolonged misalignment</td>
<td>Renewed DE bearing 7310 BECBM, flushed housing, refilled ISO VG 68</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- Never run the pump against a closed discharge. The min-flow recycle (FV-1201) protects the pump from deadhead overheating.
- Respect the interlock SEQ-1201: e.g. PSLL-1201 trips at < 0.5 barg - never defeat it without a permit.
- **Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-1201 before working on GA-1201A.**

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing       |
| --------------------------- | ------------------------ | ------------------------ | --------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Arya Wibisono (EMP-0912) | Friday, 03 April 2026 |


Notes: Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
