import time, os
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
assert API_KEY, "Falta GOOGLE_API_KEY en .env"

client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1"})

user_question = (
    "Escribe un resumen con subtítulos sobre la evolución del pensamiento estratégico, "
    "incluye hitos y autores clave (~300 palabras)."
)

t0 = time.perf_counter()

stream = client.models.generate_content_stream(
    model="gemini-2.5-pro",  # <-- de tu lista (mejor para streaming)
    contents=Content(role="user", parts=[Part.from_text(text=user_question)])
)

print("=== RESPUESTA (streaming) ===")
first_token_ms = None

for event in stream:
    chunk = getattr(event, "text", None)
    if chunk:
        if first_token_ms is None:
            first_token_ms = (time.perf_counter() - t0) * 1000
        print(chunk, end="", flush=True)

total_ms = (time.perf_counter() - t0) * 1000
print("\n\n=== MÉTRICAS ===")
print("Tiempo hasta primer token (ms):", round(first_token_ms or 0.0, 1))
print("Tiempo total (ms):", round(total_ms, 1))
