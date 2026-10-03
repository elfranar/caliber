<!-- case1_doc_name: OPL-DC-3401A-02 Inerting_O2_Freeing_Below_100_ppm.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**            |                  | OPL No: **OPL-DC-3401A-02**<br/>Sheet 1 of 1 |                               |
| ------------------------------------------------------ | ------------------------------------- | ---------------- | -------------------------------------------- | ----------------------------- |
| **OPL Title**                                          | Inerting - O2 Freeing Below 100 ppm   | **Discipline**   | Process / Operations                         |                               |
| **Equipment**                                          | DC-3401A - CATALYST REDUCTION REACTOR | **Area / Unit**  | 3400 - CATALYST REDUCTION SYSTEM             |                               |
| **Related Interlock**                                  | SEQ-3401 (SIL 2)                      | **P\&ID Ref**    | TJC-LLD-PID-3401                             |                               |
| **Classification:**                                    | \[X] Basic Knowledge                  | \[ ] Improvement | \[ ] Trouble Case                            | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **inerting - o2 freeing below 100 ppm** for DC-3401A (CATALYST REDUCTION REACTOR) in the CATALYST REDUCTION SYSTEM. Hydrogen must never meet oxygen inside the reactor. Inerting is proven before any heating and again before hydrogen is admitted. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **N2 / H2 / Pd catalyst** at up to 6 barg / FV / 250 degC. Observe the following before and during the task:

- [ ] Obtain the correct operating permit and brief the shift team before the task.
- [ ] Confirm hazardous fluids are isolated / inerted as required by procedure.
- [ ] Beware of flammable, hot, or high-pressure fluids; wear the correct PPE.
- [ ] Never defeat a safety interlock or trip without an authorised override permit.
- [ ] Have emergency actions and communications ready before starting.

## 3. TOOLS & MATERIALS REQUIRED

- Operating procedure & P&ID
- Radio / communication with panel
- Gas detector (O2 / LEL) as required
- Correct PPE for the fluid handled
- Sample containers & PPE for sampling
- Permit-to-work documentation

## 4. DETAILED PROCEDURE / STEPS

| Step | Action                                                         | Check / Acceptance         |
| ---- | -------------------------------------------------------------- | -------------------------- |
| 1    | Inject nitrogen through FV-17343 into the reactor              | Permit valid & briefed     |
| 2    | Purge until the outlet O2 analyzer AI-3401 reads below 100 ppm | Parameter within limit     |
| 3    | Confirm all vent and drain paths are correctly lined up        | Interlock status confirmed |
| 4    | Log the O2 value and time before proceeding to heat-up         | Change logged on DCS       |
| 5    | If O2 will not fall, check for air ingress at manways/flanges  | Handover to next shift     |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Bed multipoint TC point 3 reading open circuit</td>
<td>Thermocouple element failed at the sheath junction</td>
<td>Replaced TC point 3 in the multipoint assembly, verified reading.</td>
  </tr>
<tr>
    <td>One heater bank drawing no current, slow heat-up</td>
<td>Electric heater element bank open circuit / element burnt</td>
<td>Replaced heater element bank, meggered, verified TIC-17343 response</td>
  </tr>
<tr>
    <td>Inerting O2 analyzer drift vs portable reference</td>
<td>Analyzer zero drift and sample dryer saturated</td>
<td>Recalibrated AI-3401 on span gas, replaced sample dryer</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- Hydrogen must never meet oxygen inside the reactor. Inerting is proven before any heating and again before hydrogen is admitted.
- Respect the interlock SEQ-3401: e.g. TSHH-3401 trips at > 230 degC - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID TJC-LLD-PID-3401 before working on DC-3401A.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor)   | Approved by (Manager)    | Date of Sharing       |
| --------------------------- | -------------------------- | ------------------------ | --------------------- |
| Panel Operator / Technician | Vino Ardiansyah (EMP-1102) | Arya Wibisono (EMP-0912) | Friday, 17 April 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
