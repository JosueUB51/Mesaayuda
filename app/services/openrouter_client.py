import httpx
from app.core.config import settings

class OpenRouterClient:
    async def chat(self, system: str, user: str) -> str:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{settings.OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.OPENROUTER_MODEL,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "temperature": 0.2,
                },
            )

        data = response.json()

        # 🔴 DEBUG CLARO EN TERMINAL
        if "choices" not in data:
            raise RuntimeError(
                f"OpenRouter error ({response.status_code}): {data}"
            )

        return data["choices"][0]["message"]["content"]
