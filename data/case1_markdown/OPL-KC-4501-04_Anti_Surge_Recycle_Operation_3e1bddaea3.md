<!-- case1_doc_name: OPL-KC-4501-04 Anti_Surge_Recycle_Operation.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**         | OPL No: **OPL-KC-4501-04**<br/>Sheet 1 of 1 |                           |                               |
| ------------------------------------------------------ | ---------------------------------- | ------------------------------------------- | ------------------------- | ----------------------------- |
| **OPL Title**                                          | **Anti-Surge / Recycle Operation** | **Discipline**                              | Process / Operations      |                               |
| **Equipment**                                          | KC-4501 - RECYCLE GAS COMPRESSOR   | **Area / Unit**                             | 4500 - RECYCLE GAS SYSTEM |                               |
| **Related Interlock**                                  | SEQ-4501 (SIL 2)                   | **P\&ID Ref**                               | TJC-LLD-PID-4501          |                               |
| **Classification:**                                    | \[ ] Basic Knowledge               | \[X] Improvement                            | \[ ] Trouble Case         | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **anti-surge** / recycle **operation** for KC-4501 (RECYCLE GAS COMPRESSOR) in the RECYCLE GAS SYSTEM. The recycle (spillback) valve protects the machine at low throughput and during start/stop; incorrect operation risks deadhead and rod overload. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

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

| Step | Action                                                          | Check / Acceptance         |
| ---- | --------------------------------------------------------------- | -------------------------- |
| 1    | Keep the anti-surge FV-4502 in auto during start-up             | Permit valid & briefed     |
| 2    | Avoid deadheading against a high discharge pressure (PSHH-4502) | Parameter within limit     |
| 3    | Watch suction PSLL-4501 for gas starvation                      | Interlock status confirmed |
| 4    | Return the machine to load slowly, closing recycle gradually    | Change logged on DCS       |
| 5    | Investigate any repeated surge cycling with the vendor curve    | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>High discharge temperature trip TSHH-4503, capacity drop</td>
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

- The recycle (spillback) valve protects the machine at low throughput and during start/stop; incorrect operation risks deadhead and rod overload.
- Respect the interlock SEQ-4501: e.g. PSLL-4504 trips at < 1.5 barg - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-4501 before working on KC-4501.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)       | Date of Sharing        |
| --------------------------- | ------------------------ | --------------------------- | ---------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Zulkarnain Hasan (EMP-0901) | Wednesday, 06 May 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
