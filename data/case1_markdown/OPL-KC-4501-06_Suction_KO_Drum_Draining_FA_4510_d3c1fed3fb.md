<!-- case1_doc_name: OPL-KC-4501-06 Suction_KO_Drum_Draining_FA_4510.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**             | OPL No: **OPL-KC-4501-06**<br/>Sheet 1 of 1 |                           |                               |
| ------------------------------------------------------ | -------------------------------------- | ------------------------------------------- | ------------------------- | ----------------------------- |
| **OPL Title**                                          | **Suction KO Drum Draining (FA-4510)** | **Discipline**                              | Process / Operations      |                               |
| **Equipment**                                          | KC-4501 - RECYCLE GAS COMPRESSOR       | **Area / Unit**                             | 4500 - RECYCLE GAS SYSTEM |                               |
| **Related Interlock**                                  | SEQ-4501 (SIL 2)                       | **P\&ID Ref**                               | TJC-LLD-PID-4501          |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                   | \[ ] Improvement                            | \[X] Trouble Case         | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **suction ko drum draining** (**fa-4510**) for KC-4501 (RECYCLE GAS COMPRESSOR) in the RECYCLE GAS SYSTEM. Liquid carried over from the KO drum destroys valves and can bend piston rods; the boot must be drained regularly. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **Ethylene/Hexane/H2** at up to 16 barg / 150 degC. Observe the following before and during the task:

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

| Step | Action                                                        | Check / Acceptance         |
| ---- | ------------------------------------------------------------- | -------------------------- |
| 1    | Drain the FA-4510 boot every shift on the operator round      | Permit valid & briefed     |
| 2    | Watch LT-4510 level and the LSHH-4510 high-high trip          | Parameter within limit     |
| 3    | Never run the compressor with a high KO drum level            | Interlock status confirmed |
| 4    | Report frequent liquid carryover to process for investigation | Change logged on DCS       |
| 5    | Confirm the auto-drain (if fitted) is functioning             | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>High discharge temperature trip<br />TSHH-4503, capacity drop</td>
<td>1st stage suction plate valve fractured</td>
<td>Replaced complete suction valve set, checked seat, leak tested</td>
  </tr>
<tr>
    <td>KC-4501 tripped on PSLL-4504 low lube oil pressure</td>
<td>Lube oil pump gears worn, relief valve set low</td>
<td>Overhauled lube oil pump, reset relief valve, verified 2.5 barg</td>
  </tr>
<tr>
    <td>High blow-by, low 2nd stage efficiency</td>
<td>PTFE piston rings worn beyond limit</td>
<td>Renewed 2nd stage PTFE piston and rider rings, honed cylinder</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- Liquid carried over from the KO drum destroys valves and can bend piston rods; the boot must be drained regularly.
- Respect the interlock SEQ-4501: e.g. PSLL-4504 trips at < 1.5 barg - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-4501 before working on KC-4501.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)       | Date of Sharing       |
| --------------------------- | ------------------------ | --------------------------- | --------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Zulkarnain Hasan (EMP-0901) | Thursday, 14 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
