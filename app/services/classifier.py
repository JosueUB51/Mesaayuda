import json
import re
import asyncio
from app.services.openrouter_client import OpenRouterClient

# =========================
# CATÁLOGOS
# =========================

DEPARTMENTS = [
    "Infraestructura",
    "Servicios Públicos",
    "Seguridad",
    "Salud",
    "Educación",
    "Finanzas",
    "Tecnología",
    "Recursos Humanos",
    "Atención Ciudadana"
]

ABBR = {
    "Infraestructura": "INF",
    "Servicios Públicos": "SP",
    "Seguridad": "SEG",
    "Salud": "SAL",
    "Educación": "EDU",
    "Finanzas": "FIN",
    "Tecnología": "TEC",
    "Recursos Humanos": "RH",
    "Atención Ciudadana": "AC"
}

# =========================
# DETECCIÓN DE AMBIGÜEDAD
# =========================

AMBIGUOUS_PHRASES = [
    "tengo un problema",
    "ayuda",
    "no funciona",
    "tengo un inconveniente",
    "necesito ayuda",
    "tengo un detalle"
]

def is_ambiguous(text: str) -> bool:
    text = text.lower().strip()
    return any(phrase in text for phrase in AMBIGUOUS_PHRASES)

# =========================
# PROMPT IA
# =========================

SYSTEM_PROMPT = f"""
You are a help desk classifier for a government institution.

RESPOND ONLY WITH VALID JSON.
DO NOT add explanations.
DO NOT use markdown.

The JSON MUST have this structure:

{{
  "department": "Tecnología",
  "emotion": "frustrado",
  "confidence": 0.0,
  "summary": "Resumen breve en español de lo que el usuario está reportando"
}}

Rules:
- department must be EXACTLY one of: {DEPARTMENTS}
- emotion must be in SPANISH: enojado | triste | neutro | frustrado | ansioso | feliz
- confidence: number between 0 and 1
- summary MUST be written in SPANISH
- summary must be an interpretation, NOT a copy of the original text
"""

# =========================
# CLASIFICADOR IA
# =========================

class ClassifierService:
    async def classify(self, text: str) -> dict:
        client = OpenRouterClient()
        raw = await client.chat(SYSTEM_PROMPT, text)

        cleaned = raw.strip()
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise RuntimeError(f"No JSON found in LLM response: {raw}")

        data = json.loads(match.group())

        dept = data.get("department")
        if dept not in DEPARTMENTS:
            raise RuntimeError(f"Departamento inválido: {dept}")

        return {
            "department": dept,
            "department_abbr": ABBR[dept],
            "emotion": data.get("emotion", "neutro"),
            "confidence": float(data.get("confidence", 0.0)),
            "summary": data.get("summary", "")
        }

# =========================
# WRAPPER SÍNCRONO (PUENTE)
# =========================

def classify_department(text: str) -> str:
    """
    Wrapper síncrono para obtener SOLO el department_abbr
    desde el clasificador async.
    """
    service = ClassifierService()

    try:
        # Caso normal (no hay loop activo)
        result = asyncio.run(service.classify(text))
    except RuntimeError:
        # Caso FastAPI / Uvicorn (loop ya activo)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(service.classify(text))

    return result["department_abbr"]
