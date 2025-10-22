import time, os
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
assert API_KEY, "Falta GOOGLE_API_KEY en .env"

# Fuerza API v1 (coincide con tus modelos disponibles)
client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1"})

user_question = "Explícame en 5 puntos qué es el pensamiento computacional y por qué es útil en carreras no técnicas."

t0 = time.perf_counter()
resp = client.models.generate_content(
    model="gemini-2.5-flash",  # <-- de tu lista
    contents=Content(
        role="user",
        parts=[Part.from_text(text=user_question)]
    )
)
elapsed_ms = (time.perf_counter() - t0) * 1000

print("=== RESPUESTA ===")
print(getattr(resp, "text", str(resp)).strip())
print("\n=== LATENCIA (ms) ===")
print(round(elapsed_ms, 1))
