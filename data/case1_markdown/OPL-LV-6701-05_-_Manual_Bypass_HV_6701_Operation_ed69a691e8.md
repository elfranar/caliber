<!-- case1_doc_name: OPL-LV-6701-05 - Manual_Bypass_HV_6701_Operation.pdf | case1_version: erse -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**              | OPL No: **OPL-LV-6701-05**<br/>Sheet 1 of 1 |                            |                               |
| ------------------------------------------------------ | --------------------------------------- | ------------------------------------------- | -------------------------- | ----------------------------- |
| **OPL Title**                                          | **Manual Bypass (HV-6701) Operation**   | **Discipline**                              | Process / Operations       |                               |
| **Equipment**                                          | LV-6701 - SEPARATOR LEVEL CONTROL VALVE | **Area / Unit**                             | 6700 - LP SEPARATOR SYSTEM |                               |
| **Related Interlock**                                  | SEQ-6701 (SIL 1)                        | **P\&ID Ref**                               | TJC-LLD-PID-6701           |                               |
| **Classification:**                                    | \[X] Basic Knowledge                    | \[ ] Improvement                            | \[ ] Trouble Case          | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **manual bypass (hv-6701) operation** for LV-6701 (SEPARATOR LEVEL CONTROL VALVE) in the LP SEPARATOR SYSTEM. The manual bypass lets operators keep the separator level safely while LV-6701 is isolated for maintenance. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **LOW CRITICAL** handling **Hexane + polymer bottoms** at up to ASME 300# / 120 degC. Observe the following before and during the task:

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

| Step | Action                                                     | Check / Acceptance         |
| ---- | ---------------------------------------------------------- | -------------------------- |
| 1    | Notify the panel and take LIC-6701 to manual               | Permit valid & briefed     |
| 2    | Crack open the bypass HV-6701 slowly                       | Parameter within limit     |
| 3    | Throttle HV-6701 to hold FA-6710 level using LT-6710       | Interlock status confirmed |
| 4    | Isolate LV-6701 (close block valves) for the work          | Change logged on DCS       |
| 5    | Reverse the steps and re-establish auto control afterwards | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>LV-6701 isolation for planned maintenance</td>
<td>Planned - bypass used to hold level</td>
<td>Lined up HV-6701 manual bypass, isolated LV-6701 safely</td>
  </tr>
<tr>
    <td>LV-6701 not responding to LIC-6701, level control lost</td>
<td>Stem seized in PTFE packing (over-tightened + fines)</td>
<td>Freed stem, renewed packing, lubricated, re-stroked and calibrated</td>
  </tr>
<tr>
    <td>Manual handwheel jack on LV-6701 seized</td>
<td>Corrosion in handwheel thread</td>
<td>Overhauled handwheel assembly, greased thread</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- The manual bypass lets operators keep the separator level safely while LV-6701 is isolated for maintenance.
- Respect the interlock SEQ-6701: e.g. LSHH-6710 trips at > 85 % - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-6701 before working on LV-6701.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor)   | Approved by (Manager)       | Date of Sharing      |
| --------------------------- | -------------------------- | --------------------------- | -------------------- |
| Panel Operator / Technician | Vino Ardiansyah (EMP-1102) | Zulkarnain Hasan (EMP-0901) | Monday, 01 June 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
