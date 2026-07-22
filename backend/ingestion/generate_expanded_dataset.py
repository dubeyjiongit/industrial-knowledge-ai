import os

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_documents")
os.makedirs(SAMPLE_DIR, exist_ok=True)

documents = {
    "company_profile_history.txt": """NORTHGATE ENERGY CORPORATION - COMPANY PROFILE & HISTORY
Facility: Northgate Refinery, Gujarat Industrial Corridor
Established: 1988 (Commissioned Phase 1: 5.0 MMTPA)
Current Refining Capacity: 15.2 MMTPA (Million Metric Tonnes Per Annum)
Ownership: Northgate Energy Ltd (70%), Industrial Infrastructure Development Corp (30%)

HISTORICAL MILESTONES:
- 1988: Initial commissioning of Crude Distillation Unit 1 (CDU-1) and Thermal Cracking Unit.
- 1996: Expansion Phase 2 added Hydrocracker Unit (HCU) and High-Pressure Steam Boiler B-201.
- 2005: Environmental modernization - installed Flue Gas Desulfurization (FGD) and Continuous Emission Monitoring.
- 2014: Digital Transformation Phase 1 - Automated SCADA systems installed across Zone A (CDU) and Zone C (Boiler House).
- 2021: Clean Fuel Expansion - Commissioned BS-VI Diesel Hydro-desulfurization (DHDS) Unit.
- 2024: Unified Asset Brain AI integration for predictive maintenance across all 6 plant operational zones.

OPERATIONAL ZONES & MAP OVERVIEW:
The Northgate Refinery covers 450 acres organized into 6 core operational zones:
- ZONE A (Crude Processing): CDU-1, VDU-1, Distillation Columns T-101, T-102.
- ZONE B (Conversion & Hydroprocessing): Hydrocracker Unit, Catalytic Reformer, Feed Gas Compressor C-102.
- ZONE C (Utilities & Power Generation): High-Pressure Steam Boilers B-201, B-202, Water Treatment Plant WTP-1.
- ZONE D (Storage & Tank Farm): Crude Oil Storage Tanks T-501 to T-510, LPG Spheres S-101 to S-104.
- ZONE E (Piping & Interconnect Network): Main Pipe Rack PR-North, Pipe Rack PR-South, Hydrocarbon Loop PL-04.
- ZONE F (Administration & Safety): Central Control Room (CCR), Main Fire Station, Safety Muster Points 1 to 4.
""",

    "plant_map_layout_spec.txt": """NORTHGATE REFINERY - GEOGRAPHIC MAP & ZONE LAYOUT SPECIFICATIONS
Document ID: SPEC-MAP-2024-V2
Classification: Plant Engineering & Facility Geography

GEOGRAPHIC MAP DIRECTORY & EQUIPMENT COORDINATES:

1. ZONE A: CRUDE PROCESSING AREA (North-West Sector, Grid N-12 to N-18)
   - Distillation Column T-101: Located at Grid N-14, East Flange. Connected to Pipe Rack PR-North.
   - Vacuum Column T-102: Located at Grid N-16, West Flange. Connected to Overhead Condenser EX-302.
   - Desalter Unit DS-01: Located at N-12, adjacent to Crude Inlet Manifold.

2. ZONE B: HYDROPROCESSING AREA (Central Sector, Grid C-05 to C-12)
   - Feed Gas Compressor C-102: Located at Grid C-08, Compressor House Bay 2.
   - Hydrocracker Reactor R-201: Located at Grid C-10, Heavy Vessel Foundation.
   - Pressure Relief Valve PRV-88: Mounted on Distillation Tower T-101 manifold at Grid C-06, Height 14 meters.

3. ZONE C: UTILITIES & BOILER HOUSE (South-East Sector, Grid S-20 to S-26)
   - High-Pressure Boiler B-201 (Natural Gas / Heavy Fuel Fired): Located at Grid S-22, Boiler Building 1. Steam Rating: 120 Tonnes/hour at 65 bar, 480°C.
   - High-Pressure Boiler B-202 (Dual Fired): Located at Grid S-24, Boiler Building 2. Steam Rating: 120 Tonnes/hour.
   - Water Demineralization Plant WTP-01: Located at Grid S-20, adjacent to Cooling Towers CT-01/02.

4. ZONE D: TANK FARM & STORAGE (South-West Sector, Grid SW-01 to SW-15)
   - Crude Storage Tanks T-501, T-502, T-503 (Floating Roof): Located at Grid SW-02 to SW-06.
   - LPG Pressurized Spheres S-101 to S-104: Located at Grid SW-12, East Dyke Wall.
   - Chemical Dosing Station CS-03: Located at Grid SW-15.

5. ZONE E: PIPE RACK INTERCONNECT NETWORK (Arterial Corridor, Grid P-01 to P-30)
   - Main Pipe Rack PR-North: Runs 850 meters East-West connecting Zone A (Crude) to Zone C (Boiler House). Carries High-Pressure Steam Line HP-ST-401 and Heavy Naphtha Line HN-202.
   - Pipe Rack PR-South: Runs 620 meters North-South connecting Tank Farm Zone D to Hydrocracker Zone B. Carries Crude Feed Line CF-101.
   - Interconnect Pipe Loop PL-04: Runs overhead along Access Road 3, carrying cooling water return CWR-302.

6. ZONE F: CONTROL & SAFETY (Central Admin Grid CA-01)
   - Central Control Room (CCR): Located at Grid CA-01 (Blast-resistant building).
   - Safety Muster Point 1: Main Gate Parking Plaza (Grid CA-05).
   - Safety Muster Point 2: South of Boiler House B-201 (Grid S-21).
   - Safety Muster Point 3: Tank Farm North Perimeter (Grid SW-01).
   - Safety Muster Point 4: Hydrocracker East Gate (Grid C-13).
""",

    "boiler_house_specifications.txt": """BOILER HOUSE OPERATIONAL & PIPING SPECIFICATIONS
Facility: Northgate Refinery, Zone C - Utilities
Equipment ID: B-201 (High-Pressure Utility Boiler 1), B-202 (High-Pressure Utility Boiler 2)

TECHNICAL PARAMETERS:
- Design Operating Pressure: 65.0 bar (942 psi)
- Superheated Steam Temperature: 480°C (896°F)
- Rated Evaporation Capacity: 120 metric tonnes per hour per boiler
- Primary Fuel: Refinery Fuel Gas (RFG) / Natural Gas
- Secondary Fuel: Low Sulfur Heavy Stock (LSHS)

PIPING & VALVE NETWORK FOR BOILER B-201:
1. High-Pressure Main Steam Header Line: Line ID ST-HP-201 (Material: SA-335 P22 Alloy Steel, 14-inch diameter). Connects Boiler B-201 to Main Pipe Rack PR-North at Grid S-22.
2. Boiler Feedwater Inlet Line: Line ID BFW-601 (Material: SA-106 Gr B Carbon Steel, 8-inch diameter). Receives treated water from Demineralization Plant WTP-01.
3. Fuel Gas Supply Line: Line ID FG-302 (Material: Carbon Steel, 6-inch diameter, equipped with automated emergency trip valve ETV-201).
4. Boiler Safety Relief Valves: PRV-201A and PRV-201B mounted on steam drum. Set pressure: 71.5 bar (1037 psi).

INSPECTION & MAINTENANCE SUMMARY FOR BOILERS:
- Boiler B-201 annual tube thickness ultrasonic testing (UT) completed in Jan 2024. Minimal wall thinning detected on superheater bend 4 (measured 5.8mm vs nominal 6.2mm).
- Boiler B-202 burner tip replacement scheduled for Q3 2024 maintenance turnaround.
""",

    "pipe_rack_network_guide.txt": """REFINERY PIPE RACK NETWORK & ROUTING DIRECTORY
Document ID: GUID-PIPE-2024
Facility: Northgate Refinery

OVERVIEW OF ARTERIAL PIPE RACK CORRIDORS:

1. MAIN PIPE RACK PR-NORTH (Length: 850m, Elevation: 6.5m to 12.0m)
   - Route: Originates at Crude Distillation Unit (Zone A), runs East along Main Plant Avenue, terminates at Boiler House B-201/B-202 (Zone C).
   - Key Lines Carried:
     * Line HP-ST-401: 14-inch High-Pressure Steam (65 bar, 480°C) from Boiler B-201 to process units.
     * Line MP-ST-202: 18-inch Medium-Pressure Steam (18 bar) for tracer heating.
     * Line HN-202: 10-inch Heavy Naphtha transfer line to Storage Tank T-503.
     * Line FG-101: 8-inch Fuel Gas Header to process furnaces.

2. PIPE RACK PR-SOUTH (Length: 620m, Elevation: 5.5m)
   - Route: Connects Tank Farm Zone D to Hydrocracker Zone B and Flare Stack FL-01.
   - Key Lines Carried:
     * Line CF-101: 24-inch Crude Oil Feed Line from Storage Tank T-501 to Desalter DS-01.
     * Line FL-901: 30-inch High-Pressure Flare Header leading to Flare Stack FL-01.

3. INTERCONNECT PIPE LOOP PL-04
   - Overhead bridge crossing Access Road 3 at Grid C-09.
   - Contains cooling water supply (CWS-301) and return (CWR-302) lines servicing Compressor C-102 and Heat Exchangers EX-301/302.

PIPE RACK LEAK & VIBRATION MONITORING:
- Vibration sensors installed on Pipe Rack PR-North at Support Pier SP-14 (near Boiler B-201 connection) due to steam hammer events during winter startup.
- Thermal expansion loops inspected bi-annually. All spring hangers on Line HP-ST-401 verified functional in Feb 2024.
""",

    "safety_emergency_handbook.txt": """NORTHGATE REFINERY - EMERGENCY RESPONSE & SAFETY HANDBOOK
Document ID: SAFE-HANDBOOK-2024
Compliance: OISD-GDN-115, Factories Act Section 41B

EMERGENCY EVACUATION & MUSTER POINT LOCATIONS:
In the event of a plant emergency alarm (Continuous Siren), all personnel must immediately proceed upwind to designated Muster Points:

- MUSTER POINT 1 (Main Gate Plaza - Grid CA-05): Primary evacuation assembly point for Administrative Building, Central Laboratory, and Visitors.
- MUSTER POINT 2 (South of Boiler House - Grid S-21): Primary assembly point for Zone C (Boiler B-201/B-202), Utilities, and Water Treatment Plant.
- MUSTER POINT 3 (Tank Farm North Gate - Grid SW-01): Primary assembly point for Zone D Tank Farm personnel.
- MUSTER POINT 4 (Hydrocracker East Gate - Grid C-13): Primary assembly point for Zone B (Compressor C-102, Hydrocracker R-201).

CRITICAL EMERGENCY CONTACT NUMBERS:
- Main Emergency Control Center (ECC): Ext. 3333 / Direct +91-265-2993333
- Fire Station (Zone F): Ext. 2222
- Medical Center / Occupational Health: Ext. 1111
- Plant Shift Manager (24x7): Ext. 4444

HAZARDOUS SUBSTANCES & TOXIC GAS SAFETY (H2S & HYDROCARBONS):
- Hydrogen Sulfide (H2S) Sensors installed in Hydrocracker Zone B (Grid C-08 near Compressor C-102). Low alarm at 10 ppm, High alarm at 20 ppm.
- Personal H2S monitors mandatory for entry into Zone B and Zone D.
- Self-Contained Breathing Apparatus (SCBA) stations located at Boiler House B-201 entrance and Compressor House C-102 control room.
"""
}

def generate_docs():
    print("Generating expanded company history, plant map, boiler, and piping documents...")
    for filename, content in documents.items():
        filepath = os.path.join(SAMPLE_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created: {filename} ({len(content)} bytes)")

if __name__ == "__main__":
    generate_docs()
