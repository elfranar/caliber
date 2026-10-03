<!-- case1_doc_name: OPL-YD-2301-06 - Outlet_Moisture_Control_Retention_Time_M.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                             | OPL No: **OPL-YD-2301-06**<br/>Sheet 1 of 1 |                             |                               |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------- | --------------------------- | ----------------------------- |
| **OPL Title**                                          | **Outlet Moisture Control & Retention Time (MT-2306)** | **Discipline**                              | Process / Operations        |                               |
| **Equipment**                                          | YD-2301 - POLYMER FLUID BED DRYER                      | **Area / Unit**                             | 2300 - POWDER DRYING SYSTEM |                               |
| **Related Interlock**                                  | SEQ-5500 (SIL 2)                                       | **P\&ID; Ref**                              | TJC-LLD-PID-2301            |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                                   | \[X] Improvement                            | \[ ] Trouble Case           | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **outlet moisture control & retention time (**mt-2306**)** for YD-2301 (POLYMER FLUID BED DRYER) in the POWDER DRYING SYSTEM. The product specification is below 300 ppm moisture. Rising outlet moisture means lost drying and off-spec powder. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **Polymer powder / LP Steam** at up to 6 barg (shell) / 150 degC. Observe the following before and during the task:

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

| Step | Action                                                              | Check / Acceptance         |
| ---- | ------------------------------------------------------------------- | -------------------------- |
| 1    | Read the MT-2306 outlet moisture every shift                        | Permit valid & briefed     |
| 2    | If moisture rises above 300 ppm, check steam pressure PT-2304 first | Parameter within limit     |
| 3    | Verify drum speed and hence retention time is correct               | Interlock status confirmed |
| 4    | Cross-check against the daily lab moisture sample                   | Change logged on DCS       |
| 5    | Adjust feed rate or steam to bring moisture back in spec            | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Steam and powder leaking at YD-2301 discharge gland</td>
<td>PTFE 4526L gland packing worn beyond service limit</td>
<td>Replaced 8 pcs PTFE 4526L packing, staggered joints, re-nipped after</td>
  </tr>
<tr>
    <td>Minor powder weep at feed-end gland</td>
<td>PTFE 4505L packing hardened and worn</td>
<td>Renewed 2 pcs PTFE 4505L feed-end packing</td>
  </tr>
<tr>
    <td>Scheduled proof test of dryer outlet high-high temperature trip</td>
<td>Set-point within tolerance, minor zero drift corrected</td>
<td>Recalibrated TSHH-2301 to 125 degC and function tested to logic</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- The product specification is below 300 ppm moisture. Rising outlet moisture means lost drying and off-spec powder.
- Respect the interlock SEQ-5500: e.g. TSHH-2301 trips at > 125 degC - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-2301 before working on YD-2301.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)       | Date of Sharing          |
| --------------------------- | ------------------------ | --------------------------- | ------------------------ |
| Panel Operator / Technician | Yudha Permana (EMP-1124) | Zulkarnain Hasan (EMP-0901) | Wednesday, 22 April 2026 |


Cross-ref tag YD-2301 across Datasheet, GA, P&ID; Interlock and Maintenance History.
