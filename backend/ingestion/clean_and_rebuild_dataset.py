import os
import sys
import shutil
import sqlite3

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.dirname(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from parse_documents import DocumentParser
from chunk_text import TextChunker
from extract_entities import EntityExtractor
from storage.vector_store import vector_store, VECTOR_DB_PATH
from storage.knowledge_graph import kg_store, DB_PATH

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SAMPLE_DIR = os.path.join(ROOT_DIR, "sample_documents")

master_documents = {
    "01_refinery_working_and_parts_guide.txt": """NORTHGATE REFINERY - COMPREHENSIVE WORKING & PARTS GUIDE
Document ID: MASTER-GUIDE-01
Language: Plain English / Educational Overview

1. WHAT IS AN OIL REFINERY? (IN SIMPLE TERMS)
An Oil Refinery is a chemical factory that receives thick, black, raw Crude Oil from the ground and cleans, boils, separates, and transforms it into everyday fuels:
- LPG (Liquefied Petroleum Gas): Household cooking gas.
- Gasoline (Petrol): Fuel for cars and motorbikes.
- Jet Fuel (Kerosene): Fuel for airplanes.
- Diesel: Fuel for trucks, buses, and heavy machinery.
- Heavy Fuel Oil: Fuel for cargo ships and power stations.
- Asphalt / Bitumen: Heavy black tar used to pave roads.

2. THE 7 MAIN SECTIONS & ALL ESSENTIAL PARTS OF THE REFINERY:

SECTION 1: CRUDE OIL RECEIVING & STORAGE (TANK FARM)
- What it does: Holds millions of liters of raw crude oil delivered by ships or pipelines.
- Essential Parts:
  * Storage Tanks T-501 to T-503: Large cylindrical steel tanks with floating roofs to prevent gas leaks.
  * Booster Pumps P-101: Pumps crude oil out of storage into processing lines.

SECTION 2: DESALTING & PRE-HEATING UNIT
- What it does: Washes salt, sand, and water out of raw crude oil.
- Why it is needed: Salt and water cause severe rust and corrosion inside steel pipes and boiling towers.
- Essential Parts:
  * Desalter Vessel DS-01: Uses high-voltage electric fields and fresh water injection to extract salt particles.

SECTION 3: PRIMARY DISTILLATION (THE MAIN BOILING TOWER)
- What it does: Boils crude oil at 370°C and separates it into different fuels based on boiling points.
- Essential Parts:
  * Pre-Heat Furnace F-101: Gas-fired oven that heats crude oil to boiling temperature.
  * Distillation Tower T-101: 45-meter tall vertical tower containing metal trays. Lighter fuels (petrol, naphtha) rise to the top; heavy diesel and gasoil sink to the bottom.

SECTION 4: VACUUM DISTILLATION (SECONDARY BOILING COLUMN)
- What it does: Takes the thick residue at the bottom of Tower T-101 and boils it again under a vacuum (low pressure) to extract heavy vacuum gas oil without burning it.
- Essential Parts:
  * Vacuum Column T-102: Wide column operating under low pressure.
  * Overhead Condenser EX-302: Cools vaporized vacuum gas oils into liquid fuel stock.

SECTION 5: CONVERSION & CRACKING (HYDROCRACKER UNIT)
- What it does: Takes cheap, heavy leftover oil and cracks (breaks) large molecules into valuable petrol and diesel using high heat, hydrogen gas, and heavy pressure.
- Essential Parts:
  * Feed Gas Compressor C-102: Motor-driven gas pump supplying high-pressure hydrogen to the reactor.
  * Hydrocracker Reactor R-201: Heavy steel pressure vessel where chemical cracking occurs.

SECTION 6: UTILITIES & POWER GENERATION (THE ENGINE OF THE PLANT)
- What it does: Produces high-pressure steam, electricity, and cooling water to power all plant machines.
- Essential Parts:
  * High-Pressure Boilers B-201 & B-202: Steam generators producing superheated steam at 65 bar (480°C).
  * Water Treatment Plant WTP-01: Purifies water so no scale builds up inside steam boilers.

SECTION 7: INTERCONNECTING PIPE RACKS & EMERGENCY FLARE STACK
- What it does: Moves oil, steam, and gas safely across the plant and burns off excess gas during emergencies.
- Essential Parts:
  * Main Pipe Rack PR-North: 850-meter elevated steel bridge carrying steam and fuel pipes.
  * Flare Stack FL-01: 100-meter tall safety tower with a pilot flame at top to safely burn excess pressure gas.
  * Safety Muster Points 1 to 4: Safe assembly areas where workers assemble during emergency alarms.
""",

    "02_plant_map_and_zones_guide.txt": """NORTHGATE REFINERY - GEOGRAPHIC MAP & ZONE DIRECTORY
Document ID: MASTER-MAP-02
Location: Gujarat Industrial Corridor (GPS: 22.3072° N, 73.1812° E)

PLANT MAP OPERATIONAL ZONES & GRID DIRECTORY:

1. ZONE A: CRUDE PROCESSING AREA (North-West Sector, Grid N-12 to N-18)
   - Distillation Column T-101 (Grid N-14): Main boiling tower.
   - Vacuum Column T-102 (Grid N-16): Secondary low-pressure boiling tower.
   - Desalter DS-01 (Grid N-12): Raw crude desalting vessel.

2. ZONE B: HYDROPROCESSING AREA (Central Sector, Grid C-05 to C-12)
   - Feed Gas Compressor C-102 (Grid C-08): Hydrogen gas compressor in Bay 2.
   - Hydrocracker Reactor R-201 (Grid C-10): Conversion reactor vessel.
   - Pressure Relief Valve PRV-88 (Grid C-06): Mounted on T-101 manifold at 14m height.

3. ZONE C: UTILITIES & BOILER HOUSE (South-East Sector, Grid S-20 to S-26)
   - High-Pressure Boiler B-201 (Grid S-22): 120 T/h 65-bar superheated steam boiler.
   - High-Pressure Boiler B-202 (Grid S-24): Dual-fired standby utility boiler.
   - Demin Water Plant WTP-01 (Grid S-20): Boiler feedwater purification plant.

4. ZONE D: TANK FARM & STORAGE (South-West Sector, Grid SW-01 to SW-15)
   - Crude Storage Tanks T-501, T-502, T-503 (Grid SW-02): Floating roof crude storage tanks.
   - LPG Spheres S-101 to S-104 (Grid SW-12): Pressurized cooking gas storage spheres.

5. ZONE E: PIPE RACK INTERCONNECT NETWORK (Arterial Corridor, Grid P-01 to P-30)
   - Main Pipe Rack PR-North: 850m overhead steel pipe bridge carrying 65-bar steam (Line ST-HP-201).
   - Pipe Rack PR-South: 620m pipe rack carrying Crude Feed Line CF-101.
   - Interconnect Loop PL-04: Overhead bridge carrying cooling water lines CWS-301 / CWR-302.

6. ZONE F: CONTROL & SAFETY CENTRE (Central Admin Grid CA-01)
   - Central Control Room (CCR): Blast-resistant main control building.
   - Muster Point 1 (Grid CA-05): Main Gate Assembly Plaza.
   - Muster Point 2 (Grid S-21): Boiler House Assembly Point.
   - Muster Point 3 (Grid SW-01): Tank Farm Assembly Point.
   - Muster Point 4 (Grid C-13): Hydrocracker Assembly Point.
""",

    "03_refinery_malfunctions_and_repairs_history.txt": """NORTHGATE REFINERY - CHRONOLOGICAL MALFUNCTION & REPAIR HISTORY (2018 - 2024)
Document ID: MASTER-HISTORY-03
Facility: Northgate Refinery

INCIDENT & REPAIR LOG:

1. INCIDENT #MAL-2018-042 (Date: 14-May-2018)
   - Equipment: High-Pressure Boiler B-201 (Zone C Utilities)
   - Supervised By: Lead Thermal Engineer Rajesh Sharma
   - Problem: High flue gas temperature (520°C) due to soot accumulation on superheater tubes.
   - Action Taken: Boiler offline for 18 hours. Soot blowers serviced, tube bundle hydro-cleaned.
   - Downtime: 18.0 hours. Status: Resolved.

2. INCIDENT #MAL-2020-109 (Date: 22-Aug-2020)
   - Equipment: Distillation Column T-101 (Zone A Crude Area)
   - Supervised By: Lead Process Engineer Inspector Maria Santos
   - Problem: Pressure differential spike across Tray 14 to Tray 20 causing liquid flooding.
   - Action Taken: Column throughput reduced by 25%. Damaged bubble-cap tray replaced during shutdown.
   - Downtime: 8.5 hours. Status: Resolved.

3. INCIDENT #MAL-2022-074 (Date: 11-Nov-2022)
   - Equipment: Boiler Feed Pump P-401B (Zone C)
   - Supervised By: Lead Mechanical Engineer Sarah Jenkins
   - Problem: Mechanical seal face cracking caused by dry running.
   - Action Taken: Standby Pump P-401A auto-started with zero plant interruption. Mechanical seal MS-8840 replaced on P-401B.
   - Downtime: 4.0 hours. Status: Resolved.

4. INCIDENT #MAL-2023-0847 (Date: 14-Jul-2023)
   - Equipment: Feed Gas Compressor C-102 (Zone B Hydrocracker)
   - Supervised By: Lead Mechanical Engineer Sarah Jenkins & Tech M. Bora
   - Problem: Severe knocking sound and discharge pressure drop (142 psi vs 155-165 psi spec) caused by monsoon moisture entering lube oil.
   - Action Taken: Worn discharge valve plate replaced (Part# CV-2210). Lube oil flushed and refilled with synthetic ISO VG 46 oil.
   - Downtime: 6.5 hours. Status: Resolved.

5. INCIDENT #MAL-2024-012 (Date: 18-Feb-2024)
   - Equipment: Heat Exchanger EX-301 (Zone E Loop PL-04)
   - Supervised By: Lead Thermal Engineer Rajesh Sharma
   - Problem: Tube-to-tubesheet joint weeping detected during NDT pressure monitoring.
   - Action Taken: Exchanger isolated via bypass valves. 3 leaking tubes plugged with brass tapered plugs. Hydro-tested at 450 psi.
   - Downtime: 12.0 hours. Status: Resolved.
""",

    "04_engineer_supervision_and_operating_log.txt": """NORTHGATE REFINERY - LEAD ENGINEER SUPERVISION DIRECTORY
Document ID: MASTER-ENGINEERS-04

LEAD ENGINEERS & OPERATIONAL JURISDICTIONS:

1. DR. ARIS THORNE - CHIEF RELIABILITY ENGINEER & SCADA DIRECTOR
   - Responsibility: Plant-wide Reliability Intelligence, SCADA Integration, Automation & AI Systems.
   - Approves: Overall plant risk scores, predictive maintenance schedules, and AI Knowledge Brain ingestion standards.

2. SARAH JENKINS - LEAD MECHANICAL ENGINEER (ROTATING EQUIPMENT)
   - Responsibility: Zone B (Compressor C-102) & Zone C (Boiler Feed Pumps P-401A/B, Reflux Pumps P-4B).
   - Oversees: Laser alignment per SOP-PUMP-04, mechanical seal replacements, compressor valve overhauls, and vibration analysis.

3. RAJESH SHARMA - LEAD THERMAL & UTILITIES ENGINEER
   - Responsibility: Zone C Utilities (High-Pressure Boilers B-201, B-202, Water Plant WTP-01) & Zone E Heat Exchangers (EX-301, EX-302).
   - Oversees: Superheated steam temperature control (480°C), boiler water chemistry sign-offs, soot blower maintenance, and furnace efficiency audits.

4. MARIA SANTOS - LEAD PROCESS & QUALITY INSPECTION ENGINEER
   - Responsibility: Zone A Crude Distillation (Tanks T-501 to T-503, Columns T-101, T-102) & Safety Relief Valves (PRV-88, PRV-201A/B).
   - Oversees: Annual OISD-116 relief valve set pressure testing (250 psi), vessel wall thickness ultrasonic testing (UT), and product quality compliance.

5. VIKRAM PATEL - LEAD SAFETY & EMERGENCY RESPONSE OFFICER
   - Responsibility: Zone F (Central Control Room, Fire Station) & Safety Muster Points 1 to 4.
   - Oversees: Lockout/Tagout (LOTO) safety permits, H2S gas detector calibrations (10 ppm low / 20 ppm high alarm), and Emergency Shutdown (ESD) drills.
""",

    "05_master_plant_logbook_2023_2024.txt": """NORTHGATE REFINERY - MASTER SHIFT LOGBOOK
Document ID: MASTER-LOGBOOK-05
Location: Central Control Room (CCR)

SHIFT LOG SUMMARY & OPERATING RECORDS:

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

    "06_emergency_shutdown_and_safety_protocol.txt": """NORTHGATE REFINERY - EMERGENCY SHUTDOWN (ESD) & SAFETY PROTOCOLS
Document ID: MASTER-SAFETY-06
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

def clean_and_rebuild():
    print("Step 1: Removing all old files in sample_documents/...")
    if os.path.exists(SAMPLE_DIR):
        shutil.rmtree(SAMPLE_DIR)
    os.makedirs(SAMPLE_DIR, exist_ok=True)

    print("Step 2: Writing 6 clean master documents into sample_documents/...")
    for filename, content in master_documents.items():
        filepath = os.path.join(SAMPLE_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created master doc: {filename} ({len(content)} bytes)")

    print("Step 3: Clearing old vector database and knowledge graph tables...")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM documents")
        conn.execute("DELETE FROM entities")
        conn.execute("DELETE FROM triples")
        conn.commit()

    with sqlite3.connect(VECTOR_DB_PATH) as conn:
        conn.execute("DELETE FROM chunks")
        conn.commit()

    # Re-initialize DB tables
    new_kg = kg_store.__class__()
    new_vec = vector_store.__class__()

    print("Step 4: Re-ingesting ONLY the 6 clean master documents into Vector Store & Knowledge Graph...")
    ingested_files = []
    for filename in sorted(os.listdir(SAMPLE_DIR)):
        if filename.endswith(".txt"):
            file_path = os.path.join(SAMPLE_DIR, filename)
            parsed = DocumentParser.parse_file(file_path)
            doc_id = filename.split("_")[0] + "_master"

            chunks = TextChunker.chunk_document(
                doc_id=doc_id,
                filename=filename,
                text=parsed['text']
            )

            new_vec.add_chunks(chunks)
            EntityExtractor.process_and_store(
                doc_id=doc_id,
                filename=filename,
                text=parsed['text']
            )
            new_kg.add_document(
                doc_id=doc_id,
                filename=filename,
                doc_type=parsed['doc_type'],
                chunk_count=len(chunks)
            )
            ingested_files.append(filename)

    stats = new_kg.get_stats()
    print(f"CLEAN DATASET REBUILD COMPLETE! Total docs: {stats['total_documents']}, Entities: {stats['total_entities']}, Triples: {stats['total_triples']}")

if __name__ == "__main__":
    clean_and_rebuild()
