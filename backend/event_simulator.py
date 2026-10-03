"""
Real-Time Telemetry & Proactive Event-Driven Alert Generator
PT Chandra Asri Pacific Tbk - CALIBER 2026

Simulates streaming DCS sensor telemetry across 4 operational instrumentation points:
- PT-1201 (Inlet Header Suction Pressure - Trip < 0.50 barg)
- PDT-1201 (Suction Strainer Y-1201 Differential Pressure - Trip > 0.60 bar)
- TT-1201 (Drive-End Bearing Thermocouple Temperature - Trip > 85.0 °C)
- VT-1201 (Radial Vibration Velocity RMS - Trip > 7.10 mm/s)

Supports anomaly triggering, step-by-step advance, and reset across all sensors.
Pushes contextual failure memory (RCA match) and tactical mitigation mandates autonomously.
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional

SENSOR_CONFIGS: Dict[str, Dict[str, Any]] = {
    "PT-1201": {
        "tag_id": "PT-1201",
        "name": "Suction Sensor PT-1201",
        "desc": "Inlet Header to Hexane Feed Pump GA-1201A",
        "unit": "barg",
        "normal_val": 1.18,
        "setpoint": 1.20,
        "low_alarm": 0.80,
        "trip_limit": 0.50,
        "warn_is_lower": True,
        "collapse_steps": [0.76, 0.64, 0.53, 0.44],
        "alert_id": "ALT-PT1201-DEGRADATION",
        "matched_incident_id": "INC-2025-0814",
        "incident_title": "August 2025 Seal Gland Leak & Cavitation Precedent",
        "similarity_score": 0.94,
        "recommended_action": "Verify auto-start of standby pump GA-1201B via Interlock EFF-5. Inboard strainer Y-1201 choking suspected.",
        "affected_downstream_units": ["DC-4501 (1st Polymerization Reactor)", "KC-4501 (Recycle Gas Compressor)"],
        "sop_reference": "TJC-LLD-IL-GA-1201A (SEQ-1201 Cause T1) & SOP-PE-GA1201-042"
    },
    "PDT-1201": {
        "tag_id": "PDT-1201",
        "name": "Diff Pressure Sensor PDT-1201",
        "desc": "Suction Strainer Y-1201 Choke Indicator",
        "unit": "bar",
        "normal_val": 0.18,
        "setpoint": 0.15,
        "low_alarm": 0.45,
        "trip_limit": 0.60,
        "warn_is_lower": False,
        "collapse_steps": [0.38, 0.48, 0.58, 0.72],
        "alert_id": "ALT-PDT1201-CLOGGING",
        "matched_incident_id": "INC-2025-0814",
        "incident_title": "Suction Strainer Y-1201 Polymer Carryover Clogging",
        "similarity_score": 0.96,
        "recommended_action": "Strainer DP > 0.45 bar indicates polymer carryover. Immediately prepare standby suction strainer line and execute backwash procedure per OPL-04 & SOP-PE-GA1201-042.",
        "affected_downstream_units": ["GA-1201A Hexane Feed Pump (Suction Starvation)", "DC-4501 Reactor Feed Loop"],
        "sop_reference": "OPL-GA-1201A-04 & SOP-PE-GA1201-042 Rev 3.0"
    },
    "TT-1201": {
        "tag_id": "TT-1201",
        "name": "DE Bearing Temp Sensor TT-1201",
        "desc": "GA-1201A Drive-End (DE) Bearing Thermocouple",
        "unit": "°C",
        "normal_val": 54.8,
        "setpoint": 55.0,
        "low_alarm": 75.0,
        "trip_limit": 85.0,
        "warn_is_lower": False,
        "collapse_steps": [68.0, 78.5, 84.0, 91.2],
        "alert_id": "ALT-TT1201-OVERHEAT",
        "matched_incident_id": "INC-2024-0312",
        "incident_title": "Drive-End Bearing Lube Degradation & Coupling Misalignment",
        "similarity_score": 0.91,
        "recommended_action": "Bearing temp exceeding 75°C alarm threshold. Check lube oil level in constant level oiler, verify cooling water flow, and schedule laser alignment check per OPL-03.",
        "affected_downstream_units": ["GA-1201A Drive Motor (30 kW)", "Pump Mechanical Seal Chamber"],
        "sop_reference": "OPL-GA-1201A-03 & Vendor Manual Flowserve Durco Mark 3"
    },
    "VT-1201": {
        "tag_id": "VT-1201",
        "name": "Vibration Velocity Sensor VT-1201",
        "desc": "GA-1201A Radial Bearing Vibration (ISO 10816)",
        "unit": "mm/s",
        "normal_val": 2.15,
        "setpoint": 2.10,
        "low_alarm": 4.50,
        "trip_limit": 7.10,
        "warn_is_lower": False,
        "collapse_steps": [3.80, 4.90, 6.20, 8.40],
        "alert_id": "ALT-VT1201-VIBRATION-SURGE",
        "matched_incident_id": "INC-2025-0814",
        "incident_title": "Impeller Imbalance & Cavitation Shock Pulse Trip",
        "similarity_score": 0.95,
        "recommended_action": "Vibration velocity exceeding ISO 10816 Zone C alarm (4.5 mm/s). Inspect for NPSHa cavitation margin, verify soft foot (<0.05 mm), and check coupling condition per OPL-07.",
        "affected_downstream_units": ["GA-1201A Drive Shaft", "Mechanical Seal Dual Cartridge"],
        "sop_reference": "OPL-GA-1201A-07 (Baseline Vibration Monitoring)"
    },
    "TE-2301": {
        "tag_id": "TE-2301",
        "name": "Dryer Temp Sensor TE-2301",
        "desc": "Polymer Fluid Bed Dryer YD-2301 Temperature",
        "unit": "°C",
        "normal_val": 85.0,
        "setpoint": 86.0,
        "low_alarm": 105.0,
        "trip_limit": 115.0,
        "warn_is_lower": False,
        "collapse_steps": [98.0, 107.0, 112.0, 118.0],
        "alert_id": "ALT-TE2301-HIGH",
        "matched_incident_id": "INC-2023-1102",
        "incident_title": "Polymer Agglomeration due to High Drying Temp",
        "similarity_score": 0.92,
        "recommended_action": "Reduce steam flow to heating coils. Verify nitrogen purge rate. Check for blockages in the dryer exhaust.",
        "affected_downstream_units": ["Polymer Storage Silos", "Extrusion Feed"],
        "sop_reference": "SOP-YD2301-TEMP-01"
    },
    "TE-3401": {
        "tag_id": "TE-3401",
        "name": "Reactor Bed Temp TE-3401",
        "desc": "Catalyst Reduction Reactor DC-3401A Bed Temp",
        "unit": "°C",
        "normal_val": 130.0,
        "setpoint": 130.0,
        "low_alarm": 140.0,
        "trip_limit": 150.0,
        "warn_is_lower": False,
        "collapse_steps": [136.0, 142.0, 148.0, 155.0],
        "alert_id": "ALT-TE3401-RUNAWAY",
        "matched_incident_id": "INC-2022-0518",
        "incident_title": "Local Runaway Reaction due to Uneven Homogenisation",
        "similarity_score": 0.98,
        "recommended_action": "Immediately stop hydrogen admission. Increase nitrogen carrier flow to cool the bed. Ensure all TE-3401-1.8 thermocouples are within 15°C of each other.",
        "affected_downstream_units": ["Catalyst Dosing System", "Main Polymerization Reactor"],
        "sop_reference": "OPL-DC-3401A-03"
    },
    "PT-4501": {
        "tag_id": "PT-4501",
        "name": "Discharge Pressure PT-4501",
        "desc": "Recycle Gas Compressor KC-4501 Discharge",
        "unit": "barg",
        "normal_val": 15.5,
        "setpoint": 15.0,
        "low_alarm": 18.0,
        "trip_limit": 20.0,
        "warn_is_lower": False,
        "collapse_steps": [16.8, 18.5, 19.8, 21.5],
        "alert_id": "ALT-PT4501-SURGE",
        "matched_incident_id": "INC-2024-0105",
        "incident_title": "Compressor Surge due to Blocked Discharge Valve",
        "similarity_score": 0.95,
        "recommended_action": "Open anti-surge valve fully. Check discharge piping for blockages. Verify seal gas pressure.",
        "affected_downstream_units": ["Gas Loop Cooler", "Reactor Feed"],
        "sop_reference": "SOP-KC4501-SURGE-02"
    },
    "TT-5601": {
        "tag_id": "TT-5601",
        "name": "Tube Skin Temp TT-5601",
        "desc": "Solvent Heater EA-5601 Tube Skin",
        "unit": "°C",
        "normal_val": 180.0,
        "setpoint": 175.0,
        "low_alarm": 210.0,
        "trip_limit": 230.0,
        "warn_is_lower": False,
        "collapse_steps": [195.0, 215.0, 225.0, 240.0],
        "alert_id": "ALT-TT5601-FOULING",
        "matched_incident_id": "INC-2023-0922",
        "incident_title": "Heater Tube Fouling Leading to Skin Overheat",
        "similarity_score": 0.91,
        "recommended_action": "Reduce steam input. Schedule heater decoking/cleaning. Verify hexane feed flow rate to prevent dry firing.",
        "affected_downstream_units": ["Fractionation Tower", "Flash Drum"],
        "sop_reference": "OPL-EA-5601-01"
    },
    "LT-6701": {
        "tag_id": "LT-6701",
        "name": "Separator Level LT-6701",
        "desc": "Separation Level Control LV-6701",
        "unit": "%",
        "normal_val": 50.0,
        "setpoint": 50.0,
        "low_alarm": 85.0,
        "trip_limit": 95.0,
        "warn_is_lower": False,
        "collapse_steps": [75.0, 88.0, 93.0, 98.0],
        "alert_id": "ALT-LT6701-FLOODING",
        "matched_incident_id": "INC-2025-0214",
        "incident_title": "Separator Flooding due to Stuck LV-6701 Positioner",
        "similarity_score": 0.94,
        "recommended_action": "Switch LV-6701 to manual and open bypass valve. Inspect instrument air supply to valve positioner.",
        "affected_downstream_units": ["Overhead Compressor", "Flare System"],
        "sop_reference": "SOP-LV6701-LVL-04"
    },
    "VT-7801": {
        "tag_id": "VT-7801",
        "name": "Fan Vibration VT-7801",
        "desc": "Cooling Tower Fan CT-7801 Gearbox",
        "unit": "mm/s",
        "normal_val": 2.5,
        "setpoint": 2.0,
        "low_alarm": 6.0,
        "trip_limit": 9.0,
        "warn_is_lower": False,
        "collapse_steps": [4.5, 6.5, 8.5, 11.0],
        "alert_id": "ALT-VT7801-VIB",
        "matched_incident_id": "INC-2024-0711",
        "incident_title": "Cooling Fan Blade Imbalance and Gearbox Wear",
        "similarity_score": 0.93,
        "recommended_action": "Trip fan motor CT-7801 immediately. Start standby cooling cell. Inspect fan blades for damage and gearbox for oil level.",
        "affected_downstream_units": ["Plant Cooling Water Header"],
        "sop_reference": "SOP-CT7801-VIB-01"
    },
    "LT-8901": {
        "tag_id": "LT-8901",
        "name": "Accumulator Level LT-8901",
        "desc": "Solvent Fractionation FA-8901 Accumulator",
        "unit": "%",
        "normal_val": 45.0,
        "setpoint": 45.0,
        "low_alarm": 20.0,
        "trip_limit": 10.0,
        "warn_is_lower": True,
        "collapse_steps": [30.0, 18.0, 12.0, 5.0],
        "alert_id": "ALT-LT8901-LOW",
        "matched_incident_id": "INC-2023-0405",
        "incident_title": "Loss of Reflux Flow due to Accumulator Emptying",
        "similarity_score": 0.96,
        "recommended_action": "Reduce reflux pump speed. Verify overhead condenser cooling water flow. Check for leaks in FA-8901 bottom piping.",
        "affected_downstream_units": ["Reflux Pumps", "Fractionation Tower Top"],
        "sop_reference": "OPL-FA-8901-02"
    }
}


class TelemetryEventSimulator:
    def __init__(self):
        self.active_sensor_tag: str = "PT-1201"
        self.sensor_states: Dict[str, Dict[str, Any]] = {}
        self.telemetry_history: List[Dict[str, Any]] = []
        self.sensor_histories: Dict[str, List[Dict[str, Any]]] = {}

        for tag, cfg in SENSOR_CONFIGS.items():
            self.sensor_states[tag] = {
                "current_val": cfg["normal_val"],
                "is_degrading": False,
                "degradation_step": 0
            }

        # Keep self.current_pressure for backward compatibility
        self.current_pressure = self.sensor_states["PT-1201"]["current_val"]
        self.trip_limit = SENSOR_CONFIGS["PT-1201"]["trip_limit"]
        self.low_alarm = SENSOR_CONFIGS["PT-1201"]["low_alarm"]
        self.is_degrading = False
        self.degradation_step = 0

        self._init_history()

    def _init_history(self):
        base_time = int(time.time()) - 60
        for tag, config in SENSOR_CONFIGS.items():
            self.sensor_histories[tag] = [
                {
                    "timestamp": datetime.fromtimestamp(base_time + (index * 5)).strftime("%H:%M:%S"),
                    "current_val": config["normal_val"],
                    "pressure": config["normal_val"],
                    "status": "NORMAL",
                    "tag_id": tag,
                }
                for index in range(12)
            ]
        self.telemetry_history = self.sensor_histories["PT-1201"]

    def trigger_anomaly(self, tag: Optional[str] = None) -> Dict[str, Any]:
        target_tag = tag if tag in SENSOR_CONFIGS else self.active_sensor_tag
        self.active_sensor_tag = target_tag
        cfg = SENSOR_CONFIGS[target_tag]
        state = self.sensor_states[target_tag]

        state["is_degrading"] = True
        state["degradation_step"] = 1
        state["current_val"] = cfg["collapse_steps"][0]

        if target_tag == "PT-1201":
            self.current_pressure = state["current_val"]
            self.is_degrading = True
            self.degradation_step = 1

        return self.get_latest_status(target_tag)

    def reset_to_normal(self, tag: Optional[str] = None) -> Dict[str, Any]:
        target_tag = tag if tag in SENSOR_CONFIGS else self.active_sensor_tag
        self.active_sensor_tag = target_tag
        cfg = SENSOR_CONFIGS[target_tag]
        state = self.sensor_states[target_tag]

        state["is_degrading"] = False
        state["degradation_step"] = 0
        state["current_val"] = cfg["normal_val"]

        if target_tag == "PT-1201":
            self.current_pressure = cfg["normal_val"]
            self.is_degrading = False
            self.degradation_step = 0

        return self.get_latest_status(target_tag)

    def step_simulation(self, tag: Optional[str] = None) -> Dict[str, Any]:
        target_tag = tag if tag in SENSOR_CONFIGS else self.active_sensor_tag
        self.active_sensor_tag = target_tag
        cfg = SENSOR_CONFIGS[target_tag]
        state = self.sensor_states[target_tag]

        steps = cfg["collapse_steps"]
        if state["is_degrading"]:
            if state["degradation_step"] < len(steps):
                state["current_val"] = steps[state["degradation_step"]]
                state["degradation_step"] += 1
            else:
                state["current_val"] = steps[-1]
        else:
            state["is_degrading"] = True
            state["degradation_step"] = 1
            state["current_val"] = steps[0]

        if target_tag == "PT-1201":
            self.current_pressure = state["current_val"]
            self.is_degrading = state["is_degrading"]
            self.degradation_step = state["degradation_step"]

        return self.get_latest_status(target_tag)

    def get_latest_status(self, tag: Optional[str] = None) -> Dict[str, Any]:
        target_tag = tag if tag in SENSOR_CONFIGS else self.active_sensor_tag
        cfg = SENSOR_CONFIGS[target_tag]
        state = self.sensor_states[target_tag]

        cur_val = state["current_val"]
        now_str = datetime.now().strftime("%H:%M:%S")

        if cfg["warn_is_lower"]:
            is_pre_trip = cur_val < cfg["low_alarm"]
            is_tripped = cur_val <= cfg["trip_limit"]
            proximity = max(0.0, min(1.0, (cfg["setpoint"] - cur_val) / max(0.001, cfg["setpoint"] - cfg["trip_limit"])))
            delta_str = f"{max(0.0, cur_val - cfg['trip_limit']):.2f} {cfg['unit']}"
        else:
            is_pre_trip = cur_val > cfg["low_alarm"]
            is_tripped = cur_val >= cfg["trip_limit"]
            proximity = max(0.0, min(1.0, (cur_val - cfg["setpoint"]) / max(0.001, cfg["trip_limit"] - cfg["setpoint"])))
            delta_str = f"{max(0.0, cfg['trip_limit'] - cur_val):.2f} {cfg['unit']}"

        alert_payload = None
        if is_pre_trip:
            alert_payload = {
                "alert_id": cfg["alert_id"],
                "severity": "CRITICAL" if is_tripped else "HIGH_WARNING",
                "timestamp": now_str,
                "tag": target_tag,
                "current_val": f"{cur_val:.2f} {cfg['unit']}",
                "trip_limit": f"{cfg['trip_limit']:.2f} {cfg['unit']}",
                "delta_to_trip": delta_str,
                "matched_incident_id": cfg["matched_incident_id"],
                "incident_title": cfg["incident_title"],
                "similarity_score": cfg["similarity_score"],
                "recommended_action": cfg["recommended_action"],
                "affected_downstream_units": cfg["affected_downstream_units"],
                "sop_reference": cfg["sop_reference"]
            }

        status_str = "TRIP_INTERLOCK_ACTIVATED" if is_tripped else ("PRE_TRIP_DEGRADING" if is_pre_trip else "NORMAL")

        history = self.sensor_histories[target_tag]
        history.append({
            "timestamp": now_str,
            "current_val": round(cur_val, 3),
            "pressure": round(cur_val, 3),
            "status": status_str,
            "tag_id": target_tag,
        })
        if len(history) > 60:
            history.pop(0)
        self.telemetry_history = history

        return {
            "timestamp": now_str,
            "tag_id": target_tag,
            "sensor_name": cfg["name"],
            "current_pressure": round(cur_val, 3),  # key for frontend
            "current_val": round(cur_val, 3),
            "unit": cfg["unit"],
            "setpoint": cfg["setpoint"],
            "low_alarm": cfg["low_alarm"],
            "trip_limit": cfg["trip_limit"],
            "trip_proximity": round(proximity, 3),
            "is_pre_trip": is_pre_trip,
            "is_tripped": is_tripped,
            "telemetry_history": history[-60:],
            "proactive_alert": alert_payload
        }
