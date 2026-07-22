import os
import sys

backend_dir = os.path.dirname(os.path.dirname(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from parse_documents import DocumentParser
from chunk_text import TextChunker
from extract_entities import EntityExtractor
from storage.vector_store import vector_store
from storage.knowledge_graph import kg_store

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SAMPLE_DIR = os.path.join(ROOT_DIR, "sample_documents")

additional_documents = {
    "07_quality_assurance_and_fuel_testing_standards.txt": """NORTHGATE REFINERY - QUALITY ASSURANCE & FUEL TESTING STANDARDS
Document ID: MASTER-QUALITY-07
Location: Central Quality Control Laboratory (Building QL-01)

FUEL SPECIFICATIONS & LABORATORY TESTING PROCEDURES:

1. MOTOR SPIRIT / GASOLINE (PETROL) STANDARDS:
   - Research Octane Number (RON): Minimum 95.0 RON for Euro-VI / BS-VI grade petrol.
   - Sulfur Content: Maximum 10 ppm (parts per million) to ensure low emissions.
   - Benzene Content: Maximum 1.0% by volume.
   - Testing Frequency: Sampled every 4 hours from Distillation Column T-101 overhead stream and final storage tanks T-501/502.

2. HIGH-SPEED DIESEL (HSD) STANDARDS:
   - Cetane Index: Minimum 51.0 for engine ignition quality.
   - Density at 15°C: 820 to 845 kg/m³.
   - Flash Point: Minimum 66°C to prevent premature accidental ignition.
   - Sulfur Content: Maximum 10 ppm after hydro-desulfurization (DHDS Unit).

3. AVIATION TURBINE FUEL (ATF / JET FUEL) STANDARDS:
   - Freeze Point: Maximum -47°C (ensures fuel does not freeze at high altitudes).
   - Water Reaction & Micro-Separation: Must pass ASTM D3948 rating > 85.
   - Supervised By: Quality Lead Inspector Maria Santos.

4. OFF-SPEC PROTOCOL:
   If fuel sample fails quality specs, automated valve AV-109 diverts stream to Slop Tank T-510 for re-processing.
""",

    "08_environmental_emissions_and_waste_treatment.txt": """NORTHGATE REFINERY - ENVIRONMENTAL EMISSIONS & WASTE TREATMENT
Document ID: MASTER-ENV-08
Compliance: CPCB (Central Pollution Control Board) & ISO 14001 Standards

1. FLUE GAS DESULFURIZATION & EMISSION MONITORING:
   - Flue Gas Desulfurization (FGD) Unit: Treats exhaust gases from Boilers B-201/B-202 to remove 98.5% of Sulfur Dioxide (SO2).
   - Continuous Emission Monitoring Systems (CEMS): Transmits real-time stack emissions (SO2, NOx, Particulate Matter) directly to environmental regulators.
   - Permissible SO2 Limit: Max 50 mg/Nm³. Current refinery average: 18.2 mg/Nm³.

2. EFFLUENT TREATMENT PLANT (ETP-01):
   - Capacity: 500 cubic meters per hour of industrial wastewater.
   - Primary Treatment: Oil-Water Separators (API Separators) recover 99% of free oil.
   - Secondary Biological Treatment: Aeration basins decompose dissolved organic compounds.
   - Zero Liquid Discharge (ZLD): Treated water recycled to Cooling Towers CT-01/02.

3. CARBON DECARBONIZATION & GREEN HYDROGEN GOALS:
   - Target 2030: 15% reduction in refinery carbon intensity.
   - Green Hydrogen Pilot: 5 MW electrolyzer unit under construction at Grid S-28 to replace 10% of fossil fuel hydrogen used in Hydrocracker Reactor R-201.
""",

    "09_turnaround_maintenance_and_overhaul_manual.txt": """NORTHGATE REFINERY - MAJOR TURNAROUND MAINTENANCE MANUAL
Document ID: MASTER-TURNAROUND-09
Schedule: Quadrennial Shutdown (Every 4 Years)

MAJOR TURNAROUND OVERHAUL PROCEDURES:

1. REFINERY TURNAROUND OVERVIEW:
   - Every 4 years, the entire refinery undergoes a planned 21-day total shutdown for thorough internal vessel inspection, cleaning, tube bundle retubing, and catalyst replacement.
   - Last Turnaround Executed: October 2022 (Overhaul Code: TA-2022). Next Scheduled Turnaround: October 2026.

2. CRITICAL OVERHAUL ACTIVITIES BY UNIT:
   - Distillation Tower T-101: Internal inspection of all 45 trays. Ultrasonic thickness testing (UT) on shell walls. Replacement of corroded tray clamps.
   - Hydrocracker Reactor R-201: Unloading spent cobalt-molybdenum catalyst. Internal vessel inspection for hydrogen blistering. Loading fresh high-activity catalyst.
   - High-Pressure Boiler B-201: Hydro-testing steam drum at 97.5 bar (1.5x operating pressure). Re-tubing superheater coil bend 4.
   - Feed Gas Compressor C-102: Complete rotor pullout, dynamic balancing, and replacement of main suction and discharge valve plates.

3. SUPERVISION & PERMIT SIGN-OFFS:
   - Lead Mechanical Engineer Sarah Jenkins signs off rotating equipment overhauls.
   - Lead Thermal Engineer Rajesh Sharma signs off boiler hydro-test certifications.
   - Chief Reliability Engineer Dr. Aris Thorne issues final plant re-commissioning permit.
""",

    "10_supply_chain_and_crude_dispatch_logistics.txt": """NORTHGATE REFINERY - SUPPLY CHAIN & PRODUCT DISPATCH LOGISTICS
Document ID: MASTER-LOGISTICS-10
Facility: Marine Terminal Jetty-01 & Rail/Truck Dispatch Gantry

LOGISTICS & DISPATCH INFRASTRUCTURE:

1. CRUDE OIL INCOMING SHIPMENTS:
   - Marine Offloading Terminal Jetty-01: Accommodates Very Large Crude Carriers (VLCC) up to 300,000 DWT.
   - Crude Pipeline Line CF-101: 36-inch diameter, 42 km cross-country pipeline pumping raw crude from Jetty-01 directly to Storage Tanks T-501, T-502, T-503 in Zone D.

2. REFINED PRODUCT DISPATCH CHANNELS:
   - Cross-Country Pipeline Network: Dispatches 60% of petrol and diesel to regional distribution depots.
   - Rail Wagon Gantry (Gantry R-01): 48-wagon loading rack for bulk diesel and petrol train dispatches.
   - Truck Loading Bay (Bay T-01 to T-08): Automated bottom-loading gantries handling 350 tank trucks per day.

3. DISPATCH SECURITY & AUTOMATED WEIGHBRIDGE:
   - Automated SCADA custody transfer meters verify exact liters dispatched per truck.
   - Quality Certificate of Analysis (COA) issued by Quality Control Lab QL-01 attached to every bill of lading before gate release.
"""
}

def add_docs():
    print("Writing 4 new master documents into sample_documents/...")
    for filename, content in additional_documents.items():
        filepath = os.path.join(SAMPLE_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created doc: {filename} ({len(content)} bytes)")

    print("Ingesting new documents into Vector Store & Knowledge Graph...")
    for filename in sorted(additional_documents.keys()):
        file_path = os.path.join(SAMPLE_DIR, filename)
        parsed = DocumentParser.parse_file(file_path)
        doc_id = filename.split("_")[0] + "_master"

        chunks = TextChunker.chunk_document(
            doc_id=doc_id,
            filename=filename,
            text=parsed['text']
        )

        vector_store.add_chunks(chunks)
        EntityExtractor.process_and_store(
            doc_id=doc_id,
            filename=filename,
            text=parsed['text']
        )
        kg_store.add_document(
            doc_id=doc_id,
            filename=filename,
            doc_type=parsed['doc_type'],
            chunk_count=len(chunks)
        )

    stats = kg_store.get_stats()
    print(f"ADDITIONAL DATASET INGESTION COMPLETE! Total docs: {stats['total_documents']}, Entities: {stats['total_entities']}, Triples: {stats['total_triples']}")

if __name__ == "__main__":
    add_docs()
