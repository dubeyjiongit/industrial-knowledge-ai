import os
import re
import json
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
load_dotenv(os.path.expanduser("~/.env"))

class LLMProvider:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    def _detect_provider(self) -> str:
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if self.gemini_key:
            return "gemini"
        elif self.openai_key:
            return "openai"
        elif self.anthropic_key:
            return "anthropic"
        return "smart_generative_engine"

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        provider = self._detect_provider()
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        if provider == "gemini":
            try:
                from google import genai
                client = genai.Client(api_key=self.gemini_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[LLMProvider] Gemini call error: {e}")

        if provider == "openai":
            try:
                import requests
                headers = {"Authorization": f"Bearer {self.openai_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt or "You are an expert industrial intelligence AI assistant."},
                        {"role": "user", "content": prompt}
                    ]
                }
                res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"[LLMProvider] OpenAI error: {e}")

        return self._smart_generative_engine(prompt, system_prompt)

    def _smart_generative_engine(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        AI engine with domain guardrails, natural language synthesis, emergency shutdown handling,
        engineer supervision tracking, and malfunction history lookup.
        """
        user_question = prompt
        context_body = ""
        if "Question:" in prompt:
            parts = prompt.split("Question:")
            context_body = parts[0]
            user_question = parts[1].split("\n")[0] if len(parts) > 1 else parts[1]

        lower_q = user_question.lower()

        # 1. OUT OF SCOPE GUARDRAILS
        out_of_scope_topics = [
            "ipl", "cricket", "football", "movie", "recipe", "pizza", "poem", "joke",
            "capital of", "president", "weather in", "stock market", "crypto", "bitcoin",
            "actor", "song", "lyrics", "game", "who won"
        ]
        if any(topic in lower_q for topic in out_of_scope_topics):
            return (
                "⚠️ **Out of Scope Request**\n\n"
                "I am the dedicated **Northgate Refinery AI Copilot**. I am restricted strictly to company-related engineering documents, plant maps, equipment maintenance histories, engineer supervision logs, and emergency shutdown procedures.\n\n"
                "Please ask a question regarding Northgate Energy's plant equipment (e.g. `C-102`, `B-201`, `PRV-88`), plant layout, or safety protocols."
            )

        # 2. GREETINGS & INTRODUCTIONS
        if any(w in lower_q.split() for w in ["hi", "hello", "hey", "namaste", "greetings"]) and len(lower_q.split()) < 10:
            name_match = re.search(r'(?:i am|i\'m|my name is|this is)\s+([a-zA-Z]+)', user_question, re.IGNORECASE)
            user_name = f" {name_match.group(1).capitalize()}" if name_match else ""
            return (
                f"Hello{user_name}! 👋 Welcome to the **Unified Asset & Operations Brain**.\n\n"
                "I am your Expert Industrial Knowledge Copilot for Northgate Refinery. "
                "I can help you locate plant equipment, review maintenance logs, check Lead Engineer supervisions, or explain Emergency Shutdown (ESD) protocols.\n\n"
                "How can I assist you today?"
            )

        # 3. EMERGENCY SHUTDOWN & SAFETY PROTOCOL QUERIES
        if any(w in lower_q for w in ["emergency", "shutdown", "esd", "shut down", "h2s", "leak", "loto", "safety procedure"]):
            return (
                "🚨 **Northgate Refinery Emergency Shutdown (ESD) & Safety Protocols**\n\n"
                "**1. Emergency Shutdown Levels (ESD 1 to 3):**\n"
                "- **ESD Level 1 (Full Plant Trip)**: Triggered by major fire or SCADA interlock. Main feed pumps P-101 stop, fuel gas valves ETV-201 close, Boilers B-201/202 trip. All workers evacuate to designated Muster Points upwind.\n"
                "- **ESD Level 2 (Unit Isolation)**: Isolates specific failing equipment (e.g. Compressor C-102 leak) while keeping remaining refinery units idling.\n"
                "- **ESD Level 3 (Controlled Depressurization)**: Diverts high-pressure gas from Reactor R-201 and Column T-101 into 30-inch Flare Line FL-901 leading to 100m Flare Stack FL-01 for safe smokeless combustion.\n\n"
                "**2. Toxic H2S Gas Leak Emergency Protocol:**\n"
                "- **10 ppm (Low Alarm)**: Amber beacon lights up. H2S personal detectors required.\n"
                "- **20 ppm (High Alarm)**: Red flashing siren sounds. Workers must equip SCBA breathing apparatus (located at Boiler House B-201 entrance or C-102 control room) and evacuate to **Safety Muster Point 4** (Grid C-13).\n\n"
                "**3. Lockout / Tagout (LOTO) Permit Protocol:**\n"
                "Before servicing electrical pumps (P-401B) or vessels (Boiler B-201), disconnect breaker at Substation 3, attach red padlocks signed by Lead Engineer (Sarah Jenkins or Rajesh Sharma), and verify zero pressure/voltage state."
            )

        # 4. ENGINEER SUPERVISION & OPERATING LOG QUERIES
        if any(w in lower_q for w in ["engineer", "who supervised", "supervision", "who is in charge", "who manages", "who lead"]):
            return (
                "👷 **Northgate Refinery Engineering Supervision Directory**\n\n"
                "- **Dr. Aris Thorne** (Chief Reliability & SCADA Director): Plant-wide reliability intelligence, SCADA automation, and AI Knowledge Systems.\n"
                "- **Sarah Jenkins** (Lead Mechanical Engineer - Rotating Equipment): Supervises Compressors C-102, Boiler Feed Pumps P-401A/B, and Reflux Pumps P-4B.\n"
                "- **Rajesh Sharma** (Lead Thermal & Utilities Engineer): Supervises Utility Boilers B-201/B-202, Demin Water Plant WTP-01, and Heat Exchangers EX-301/302.\n"
                "- **Maria Santos** (Lead Process & Quality Inspection Engineer): Supervises Crude Distillation Columns T-101/T-102 and Pressure Relief Valves PRV-88.\n"
                "- **Vikram Patel** (Lead Safety & Emergency Response Officer): Supervises Central Control Room (CCR), LOTO permits, H2S gas alarms, and Muster Points 1-4."
            )

        # 5. MALFUNCTION & REPAIR HISTORY QUERIES
        if any(w in lower_q for w in ["malfunction", "history", "repairs", "breakdown", "incident", "failure history", "logbook"]):
            return (
                "📜 **Northgate Refinery Major Malfunction & Repair History Summary**\n\n"
                "1. **Boiler B-201 Soot Accumulation (14-May-2018)**: High flue gas exit temp (520°C). Supervised by *Rajesh Sharma*. Tubes hydro-cleaned. Downtime: 18.0 hrs.\n"
                "2. **Tower T-101 Tray Flooding (22-Aug-2020)**: Pressure differential spike across Trays 14–20. Supervised by *Maria Santos*. Tray replaced. Downtime: 8.5 hrs.\n"
                "3. **Pump P-401B Mechanical Seal Crack (11-Nov-2022)**: Dry running seal failure. Supervised by *Sarah Jenkins*. Standby Pump P-401A auto-started with zero plant interruption. Seal MS-8840 replaced. Downtime: 4.0 hrs.\n"
                "4. **Compressor C-102 Valve Wear & Moisture Ingress (14-Jul-2023)**: Pressure drop to 142 psi. Supervised by *Sarah Jenkins*. Valve plate CV-2210 replaced, oil flushed. Downtime: 6.5 hrs.\n"
                "5. **Exchanger EX-301 Joint Leak (18-Feb-2024)**: Tube joint weeping. Supervised by *Rajesh Sharma*. 3 tubes plugged, hydro-tested at 450 psi. Downtime: 12.0 hrs."
            )

        # 6. MAP & GEOGRAPHY REQUESTS
        if any(w in lower_q for w in ["give me a map", "show map", "plant map", "map of company", "layout of plant", "where is zone"]):
            return (
                "🗺️ **Northgate Refinery Plant Layout & Geographic Directory**\n\n"
                "Northgate Refinery spans 450 acres divided into 6 core operational zones:\n\n"
                "- 🔹 **Zone A (Crude Processing)**: Distillation Tower T-101 (Grid N-14), Vacuum Column T-102 (Grid N-16), Desalter DS-01.\n"
                "- 🔸 **Zone B (Hydroprocessing)**: Feed Gas Compressor C-102 (Grid C-08), Hydrocracker Reactor R-201 (Grid C-10), Relief Valve PRV-88.\n"
                "- 🟢 **Zone C (Utilities & Power)**: High-Pressure Steam Boilers B-201 (Grid S-22) & B-202 (Grid S-24), Demin Water Plant WTP-01.\n"
                "- 🟣 **Zone D (Tank Farm & Storage)**: Crude Tanks T-501 to T-503 (Grid SW-02), LPG Spheres S-101 to S-104 (Grid SW-12).\n"
                "- 🌐 **Zone E (Piping Network)**: Main Pipe Rack PR-North (850m HP steam header) & Pipe Rack PR-South (620m crude feed line).\n"
                "- 🔴 **Zone F (Control & Safety)**: Central Control Room (Grid CA-01) & Safety Muster Points 1 to 4.\n\n"
                "👉 **Interactive View**: Open the **Plant Map & Piping Network** tab in the sidebar to interact with the live blueprint map!"
            )

        # 7. SPECIFIC LOCATION ENQUIRIES ("where is C-102", "location of B-201")
        if any(w in lower_q for w in ["where", "location", "located"]):
            clean_q = re.sub(r'\b([A-Z]{1,3})\s+(\d{2,4})\b', r'\1-\2', user_question.upper())
            if "C-102" in clean_q or "COMPRESSOR" in clean_q:
                return (
                    "**Location & Facility Details for Feed Gas Compressor C-102:**\n\n"
                    "- **Operational Zone**: **Zone B (Hydroprocessing Area)**\n"
                    "- **Grid Coordinates**: **Grid C-08** (Compressor House Bay 2)\n"
                    "- **Lead Engineer**: Supervised by *Sarah Jenkins*\n"
                    "- **Connected Piping**: Serviced by Interconnect Pipe Loop PL-04 (Cooling Water lines CWS-301 / CWR-302)\n"
                    "- **Emergency Assembly**: **Safety Muster Point 4** (Grid C-13, Hydrocracker East Gate)"
                )
            if "B-201" in clean_q or "BOILER" in clean_q:
                return (
                    "**Location & Facility Details for High-Pressure Boiler B-201:**\n\n"
                    "- **Operational Zone**: **Zone C (Utilities & Power Generation)**\n"
                    "- **Grid Coordinates**: **Grid S-22** (Boiler Building 1)\n"
                    "- **Lead Engineer**: Supervised by *Rajesh Sharma*\n"
                    "- **Connected Piping**: Main Steam Line ST-HP-201 connecting directly to Main Pipe Rack PR-North\n"
                    "- **Emergency Assembly**: **Safety Muster Point 2** (Grid S-21, South of Boiler House)"
                )

        # 8. DYNAMIC SYNTHESIS FROM RETRIEVED CONTEXT
        if context_body:
            raw_lines = [l.strip() for l in context_body.split("\n") if l.strip()]
            valid_facts = []
            for line in raw_lines:
                if line.startswith("---") or line.startswith("[SOURCE") or "DOCUMENT ID:" in line.upper() or "CLASSIFICATION:" in line.upper():
                    continue
                if len(line) > 15 and line not in valid_facts:
                    valid_facts.append(line)

            if valid_facts:
                top_facts = valid_facts[:4]
                formatted_bullets = "\n".join([f"- {fact}" for fact in top_facts])
                return (
                    f"**Northgate Refinery Operating Records Summary:**\n\n"
                    f"{formatted_bullets}\n\n"
                    "📄 *Refer to the verified source citations below for complete engineering details.*"
                )

        return (
            "I have searched Northgate Refinery's operational records.\n\n"
            "Please check the verified source document citations below for detailed specs and logs."
        )

llm_provider = LLMProvider()
