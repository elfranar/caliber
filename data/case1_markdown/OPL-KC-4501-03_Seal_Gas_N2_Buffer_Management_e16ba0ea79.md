<!-- case1_doc_name: OPL-KC-4501-03 Seal_Gas_N2_Buffer_Management.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**          | OPL No: **OPL-KC-4501-03**<br/>Sheet 1 of 1 |                           |                               |
| ------------------------------------------------------ | ----------------------------------- | ------------------------------------------- | ------------------------- | ----------------------------- |
| **OPL Title**                                          | **Seal Gas (N2 Buffer) Management** | **Discipline**                              | Process / Operations      |                               |
| **Equipment**                                          | KC-4501 - RECYCLE GAS COMPRESSOR    | **Area / Unit**                             | 4500 - RECYCLE GAS SYSTEM |                               |
| **Related Interlock**                                  | SEQ-4501 (SIL 2)                    | **P\&ID Ref**                               | TJC-LLD-PID-4501          |                               |
| **Classification:**                                    | \[X] Basic Knowledge                | \[ ] Improvement                            | \[ ] Trouble Case         | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **seal gas (n2 buffer) management** for KC-4501 (RECYCLE GAS COMPRESSOR) in the RECYCLE GAS SYSTEM. The nitrogen buffer keeps flammable process gas out of the crankcase; loss of seal gas is a fire/explosion risk. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

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

| Step | Action                                                   | Check / Acceptance         |
| ---- | -------------------------------------------------------- | -------------------------- |
| 1    | Verify FT-4506 seal gas flow is established before start | Permit valid & briefed     |
| 2    | Maintain the buffer differential above process pressure  | Parameter within limit     |
| 3    | Watch the distance-piece vent for signs of leakage       | Interlock status confirmed |
| 4    | Respond immediately to a seal-gas low alarm              | Change logged on DCS       |
| 5    | Never run the compressor with seal gas lost              | Handover to next shift     |


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

- The nitrogen buffer keeps flammable process gas out of the crankcase; loss of seal gas is a fire/explosion risk.
- Respect the interlock SEQ-4501: e.g. PSLL-4504 trips at < 1.5 barg - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-4501 before working on KC-4501.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)       | Date of Sharing       |
| --------------------------- | ------------------------ | --------------------------- | --------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Zulkarnain Hasan (EMP-0901) | Saturday, 02 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
