import os

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_documents")
os.makedirs(SAMPLE_DIR, exist_ok=True)

documents = {
    "refinery_malfunctions_and_repairs_history.txt": """NORTHGATE REFINERY - CHRONOLOGICAL MALFUNCTION & REPAIR HISTORY (2018 - 2024)
Document ID: HIST-REPAIR-2024-FULL
Facility: Northgate Refinery, Unit 1, 2, & 3

RECORDED MALFUNCTIONS, ROOT CAUSE & REPAIR LOG:

1. INCIDENT #MAL-2018-042 (Date: 14-May-2018)
   - Equipment: High-Pressure Boiler B-201 (Zone C Utilities)
   - Supervised By: Lead Thermal Engineer Rajesh Sharma
   - Malfunction: High flue gas exit temperature (520°C vs 480°C spec) due to soot accumulation on superheater tubes.
   - Action Taken: Boiler B-201 taken offline for 18 hours. Soot blowers serviced, tube bundle hydro-cleaned.
   - Downtime: 18.0 hours. Status: Resolved.

2. INCIDENT #MAL-2020-109 (Date: 22-Aug-2020)
   - Equipment: Distillation Column T-101 (Zone A Crude Area)
   - Supervised By: Lead Process Engineer Inspector Maria Santos
   - Malfunction: Pressure differential spike across Tray 14 to Tray 20 causing liquid flooding and off-spec naphtha quality.
   - Action Taken: Column throughput reduced by 25%. Steam reboiler temperature recalibrated. Damaged bubble-cap tray replaced during Q4 shutdown.
   - Downtime: 8.5 hours. Status: Resolved.

3. INCIDENT #MAL-2022-074 (Date: 11-Nov-2022)
   - Equipment: Boiler Feed Pump P-401B (Zone C)
   - Supervised By: Lead Mechanical Engineer Sarah Jenkins
   - Malfunction: Mechanical seal face cracking caused by dry running during feedwater deaerator level drop.
   - Action Taken: Standby Pump P-401A automatically auto-started. Mechanical seal assembly (Part# MS-8840) replaced on P-401B.
   - Downtime: 4.0 hours (zero plant interruption due to P-401A auto-start). Status: Resolved.

4. INCIDENT #MAL-2023-0847 (Date: 14-Jul-2023)
   - Equipment: Feed Gas Compressor C-102 (Zone B Hydrocracker Area)
   - Supervised By: Lead Mechanical Engineer Sarah Jenkins & Tech M. Bora
   - Malfunction: Severe knocking sound and discharge pressure fluctuation (142 psi vs 155-165 psi spec). Moisture ingress during heavy monsoon rain contaminated lubrication oil.
   - Action Taken: Worn discharge valve plate replaced (Part# CV-2210). Lube oil drained, flushed, and refilled with synthetic ISO VG 46 oil.
   - Downtime: 6.5 hours. Status: Resolved.

5. INCIDENT #MAL-2024-012 (Date: 18-Feb-2024)
   - Equipment: Heat Exchanger EX-301 (Zone E / Zone B Loop PL-04)
   - Supervised By: Lead Thermal Engineer Rajesh Sharma
   - Malfunction: Tube-to-tubesheet joint weeping detected during routine NDT pressure monitoring.
   - Action Taken: Exchanger isolated via bypass valves. 3 leaking tubes plugged with brass tapered plugs. Hydro-tested at 450 psi.
   - Downtime: 12.0 hours. Status: Resolved.
""",

    "engineer_supervision_operating_log.txt": """ENGINEERING SUPERVISION & OPERATIONAL RESPONSIBILITY DIRECTORY
Document ID: DIR-ENG-SUPERVISION-2024
Facility: Northgate Refinery

LEAD ENGINEERS & OPERATIONAL JURISDICTIONS:

1. DR. ARIS THORNE - CHIEF RELIABILITY ENGINEER & SCADA DIRECTOR
   - Jurisdiction: Plant-wide Reliability Intelligence, SCADA Integration, Automation & AI Systems.
   - Key Responsibilities: Approves overall plant risk scores, predictive maintenance schedules, and AI Knowledge Brain ingestion standards.

2. SARAH JENKINS - LEAD MECHANICAL ENGINEER (ROTATING EQUIPMENT)
   - Jurisdiction: Zone B (Compressors C-102) & Zone C (Boiler Feed Pumps P-401A/B, Reflux Pumps P-4B).
   - Key Responsibilities: Oversees laser alignment per SOP-PUMP-04, mechanical seal replacements, compressor valve overhauls, and vibration analysis.

3. RAJESH SHARMA - LEAD THERMAL & UTILITIES ENGINEER
   - Jurisdiction: Zone C Utilities (High-Pressure Boilers B-201, B-202, Demin Water Plant WTP-01) & Zone E Heat Exchangers (EX-301, EX-302).
   - Key Responsibilities: Superheated steam temperature control (480°C), boiler water chemistry sign-offs, soot blower maintenance, and furnace efficiency audits.

4. MARIA SANTOS - LEAD PROCESS & QUALITY INSPECTION ENGINEER
   - Jurisdiction: Zone A Crude Distillation (Tanks T-501 to T-503, Columns T-101, T-102) & Safety Relief Valves (PRV-88, PRV-201A/B).
   - Key Responsibilities: Annual OISD-116 relief valve set pressure testing (250 psi), vessel wall thickness ultrasonic testing (UT), and product specification compliance.

5. VIKRAM PATEL - LEAD SAFETY & EMERGENCY RESPONSE OFFICER
   - Jurisdiction: Zone F (Central Control Room, Fire Station) & Plant-wide Safety Muster Points 1 to 4.
   - Key Responsibilities: Authorizes Lockout/Tagout (LOTO) permits, oversees H2S gas detector calibrations (10 ppm low / 20 ppm high alarm), and leads Emergency Shutdown (ESD) drills.
""",

    "master_plant_logbook_2023_2024.txt": """MASTER PLANT LOGBOOK - OPERATIONAL RECORDS & SHIFT HANDOVERS
Document ID: LOG-MASTER-2023-2024
Facility: Northgate Refinery, Central Control Room (CCR)

SHIFT LOG SUMMARY & OPERATING PARAMETERS:

- LOG DATE: 12-Mar-2023 | SHIFT B | OPERATOR: R. Singh | SUPERVISOR: Maria Santos
  * Event: Annual pressure relief valve inspection for PRV-88 on Distillation Tower T-101. Set pressure verified at 250 psi (+/- 3%). Tag illegible - recommendation filed for re-stamping. Compliance: OISD-116 PASS. Next due: 12-Mar-2024.

- LOG DATE: 14-Jul-2023 | SHIFT A | OPERATOR: K. Patel | SUPERVISOR: Sarah Jenkins
  * Event: Feed Gas Compressor C-102 trip on high vibration. Technician M. Bora dispatched. Found worn valve plate (CV-2210) due to monsoon moisture ingress. Valve plate replaced, lube oil flushed. Restarted successfully at 16:30 hrs.

- LOG DATE: 25-Sep-2023 | SHIFT C | OPERATOR: A. Sharma | SUPERVISOR: Sarah Jenkins
  * Event: Reflux Pump P-4B seal weeping noted. Inspection IR-2023-114 filed. Traced to 0.4mm shaft misalignment dating back to Feb overhaul. Laser alignment re-verified per SOP-P4B-02 Rev 2.

- LOG DATE: 15-Jan-2024 | SHIFT A | OPERATOR: V. Kumar | SUPERVISOR: Rajesh Sharma
  * Event: Boiler B-201 annual UT thickness audit. Superheater bend 4 measured 5.8mm vs nominal 6.2mm. Deemed safe for continued operation at 65 bar. Re-inspection scheduled for Jan 2025.

- LOG DATE: 10-May-2024 | SHIFT B | OPERATOR: R. Singh | SUPERVISOR: Vikram Patel
  * Event: Quarterly H2S sensor calibration in Zone B (Grid C-08 near C-102). Low alarm verified at 10 ppm, High alarm verified at 20 ppm. All 4 SCBA breathing apparatus stations inspected & fully charged.
""",

    "emergency_shutdown_and_safety_protocol.txt": """NORTHGATE REFINERY - EMERGENCY SHUTDOWN (ESD) & SAFETY PROTOCOLS
Document ID: SAFE-ESD-PROTOCOL-2024
Compliance: OISD-GDN-115, OSHA 1910.119 Process Safety Management

1. EMERGENCY SHUTDOWN LEVELS (ESD LEVELS 1 TO 3):

   - ESD LEVEL 1: FULL PLANT EMERGENCY TRIP (Continuous 30-Second Alarm Siren)
     * Action: Triggered automatically by major fire or SCADA system safety interlock. Main feed pumps P-101 stop. Fuel gas emergency trip valves ETV-201 close. Boilers B-201 and B-202 trip.
     * Evacuation: All non-essential personnel immediately evacuate to designated Muster Points upwind.

   - ESD LEVEL 2: UNIT ISOLATION SHUTDOWN (Intermittent Alarm Siren)
     * Action: Triggered for localized equipment failure (e.g. Compressor C-102 gas leak or Boiler B-201 tube leak). Unit motor-operated valves (MOVs) isolate the affected zone (Zone B or Zone C) while keeping remaining refinery units idling.

   - ESD LEVEL 3: CONTROLLED DEPRESSURIZATION VIA FLARE STACK FL-01
     * Action: Automated blowdown valves open, diverting high-pressure gas from Hydrocracker Reactor R-201 and Tower T-101 into 30-inch Flare Header Line FL-901 leading to 100m Flare Stack FL-01 for safe smokeless combustion.

2. TOXIC HYDROGEN SULFIDE (H2S) GAS LEAK EMERGENCY PROCEDURE:
   - If H2S sensor reads >= 10 ppm (Low Alarm): Beeping amber beacon turns on. Personnel in Zone B must equip personal H2S monitors.
   - If H2S sensor reads >= 20 ppm (High Alarm): Red flashing siren turns on. Personnel must immediately put on SCBA mask (Self-Contained Breathing Apparatus) available at Boiler House B-201 entrance or Compressor House C-102 control room and evacuate upwind to MUSTER POINT 4 (Grid C-13).

3. LOCKOUT / TAGOUT (LOTO) SAFETY PERMIT RULES:
   - Before performing maintenance on any electrical pump (e.g., P-401B) or vessel (e.g., Boiler B-201):
     1. Disconnect main breaker at Substation 3.
     2. Attach red LOTO safety padlock and tag signed by Lead Engineer (Sarah Jenkins or Rajesh Sharma).
     3. Verify zero energy state (bleed pressure valves, check zero voltage) before starting work.
"""
}

def generate_docs():
    print("Generating hypothetical malfunction history, engineer supervision, logbook, and emergency shutdown protocols...")
    for filename, content in documents.items():
        filepath = os.path.join(SAMPLE_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created: {filename} ({len(content)} bytes)")

if __name__ == "__main__":
    generate_docs()
