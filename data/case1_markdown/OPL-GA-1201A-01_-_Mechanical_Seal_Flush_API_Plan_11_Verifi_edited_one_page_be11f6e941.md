<!-- case1_doc_name: OPL-GA-1201A-01 - Mechanical_Seal_Flush_API_Plan_11_Verifi_edited_one_page.pdf | case1_version: iewed -->

| This is sample data provided for CALIBER purposes only | **ONE POINT LESSON (OPL)**                           | OPL No: **OPL-GA-1201A-01**<br/>Sheet 1 of 1 |                           |                               |
| ------------------------------------------------------ | ---------------------------------------------------- | -------------------------------------------- | ------------------------- | ----------------------------- |
| **OPL Title**                                          | **Mechanical Seal Flush (API Plan 11) Verification** | **Discipline**                               | Mechanical                |                               |
| **Equipment**                                          | GA-1201A - HEXANE FEED PUMP                          | **Area / Unit**                              | 1200 - HEXANE FEED SYSTEM |                               |
| **Related Interlock**                                  | SEQ-1201 (SIL 1)                                     | **P\&ID; Ref**                               | TJC-LLD-PID-1201          |                               |
| **Classification:**                                    | \[ ] Basic Knowledge                                 | \[ ] Improvement                             | \[X] Trouble Case         | Aspect: P-Q-C-D-\*\*S\*\*-M-E |


## 1. PURPOSE / OBJECTIVE

This One Point Lesson explains **mechanical seal flush (api plan 11) verification** for GA-1201A (HEXANE FEED PUMP) in the HEXANE FEED SYSTEM. Confirm seal flush dP > 1.5 bar before start. Low flush = seal face overheating and hexane leak to atmosphere. The lesson gives operators and technicians the key knowledge and the correct step-by-step method so the task is done safely, correctly and consistently every time.

## 2. SAFETY PRECAUTIONS

Hazard note: this equipment is **HIGH CRITICAL** handling **n-Hexane** at up to 16 barg / 80 degC. Observe the following before and during the task:

- Apply LOTO (Lock-Out Tag-Out) and prove zero energy before starting work.
- Isolate, depressurise, drain and purge the equipment; obtain a valid work permit.
- Wear the correct PPE: coverall, safety shoes, gloves, goggles and hearing protection.
- Beware of stored mechanical energy (springs, rotating inertia) and pinch points.
- Use certified lifting gear and correct manual-handling technique for heavy parts.

## 3. TOOLS & MATERIALS REQUIRED

- Standard mechanical hand tools & calibrated torque wrench
- LOTO padlocks and permit
- Laser/dial alignment kit (as applicable)
- Feeler gauges, dial indicator, seal/bearing pullers
- Correct spare parts and gaskets per the BOM
- Lifting gear and slings (certified)

## 4. DETAILED PROCEDURE / STEPS

| Step | Action                                                                      | Check / Acceptance          |
| ---- | --------------------------------------------------------------------------- | --------------------------- |
| 1    | Line up discharge flush to seal chamber and open flush isolation            | Isolation & LOTO verified   |
| 2    | Check PDI-1201 reads 1.5-2.5 bar dP across the flush orifice RO-1201        | Parts match BOM / spec      |
| 3    | Verify no visible leak or drip at the gland / seal drain                    | Torque / clearance to spec  |
| 4    | If dP low, isolate and inspect orifice RO-1201 for plugging by polymer/dirt | No leak / smooth operation  |
| 5    | Confirm quench (Plan 62) N2/steam is lined up to the outboard side          | Record in equipment history |


## 5. COMMON PROBLEMS & TROUBLESHOOTING

<table>
  <tr>
    <th>Symptom</th>
    <th>Likely Cause</th>
    <th>Action</th>
  </tr>
<tr>
    <td>Hexane leak observed at GA-1201A seal gland during operation, seal dr.</td>
<td>API Plan 11 flush orifice RO-1201 partially plugged causing seal face.</td>
<td>Replaced JC T2100 mechanical seal cartridge, cleaned flush orifice, v.</td>
  </tr>
<tr>
    <td>GA-1201A tripped on VSHH-1201 high vibration 7.4 mm/s</td>
<td>Angular misalignment 0.12 mm/100mm after foundation settlement</td>
<td>Laser re-aligned pump/motor, re-shimmed motor feet, vibration back to.</td>
  </tr>
<tr>
    <td>Bearing DE noisy with rising temperature TI-1201 trend</td>
<td>Outer race spalling on DE bearing due to prolonged misalignment</td>
<td>Renewed DE bearing 7310 BECBM, flushed housing, refilled ISO VG 68</td>
  </tr>
</table>

## 6. KEY LEARNING POINTS

- Confirm seal flush dP > 1.5 bar before start. Low flush = seal face overheating and hexane leak to atmosphere.
- Respect the interlock SEQ-1201: e.g. PSLL-1201 trips at < 0.5 barg - never defeat it without a permit.
- Always cross-check the Datasheet limits and the P&ID; TJC-LLD-PID-1201 before working on GA-1201A.
- Record the work in the equipment history so the Knowledge Hub stays the single source of truth.

| Prepared by                 | Reviewed by (Supervisor) | Approved by (Manager)    | Date of Sharing       |
| --------------------------- | ------------------------ | ------------------------ | --------------------- |
| Panel Operator / Technician | Wahyu Setiadi (EMP-1113) | Arya Wibisono (EMP-0912) | Sunday, 22 March 2026 |


Cross-ref tag GA-1201A across Datasheet, GA, P&ID, Interlock and Maintenance History.
