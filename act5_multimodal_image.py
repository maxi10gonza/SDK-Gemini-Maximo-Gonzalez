import os, mimetypes, sys
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part
from google.genai.errors import ClientError

# 1) Cargar API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("No se encontró GOOGLE_API_KEY en .env. Abre .env y asegúrate de tener:\nGOOGLE_API_KEY=tu_clave_aqui")
    sys.exit(1)

# 2) Configurar cliente (forzamos API v1)
client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1"})

# 3) Ruta de imagen
IMAGE_PATH = os.path.join("assets", "foto_comida.jpg")  # <- si cambias nombre, cámbialo aquí también

# 4) Validar existencia de imagen
if not os.path.exists(IMAGE_PATH):
    print(f"No existe la imagen en: {IMAGE_PATH}\nCópiala a esa ruta o ajusta IMAGE_PATH.")
    sys.exit(1)

# 5) Determinar MIME type
mime_type = mimetypes.guess_type(IMAGE_PATH)[0]
if mime_type is None:
    # fallback simple
    ext = os.path.splitext(IMAGE_PATH)[1].lower()
    mime_type = "image/png" if ext == ".png" else "image/jpeg"

# 6) Leer bytes
with open(IMAGE_PATH, "rb") as f:
    image_bytes = f.read()

# 7) Pregunta específica
user_question = (
    "Identifica los 3 ingredientes principales de este plato y sugiere 2 cambios concretos para hacerlo más saludable."
)

# 8) Construir contenido (IMPORTANTE: usar keywords en Part)
contents = Content(
    role="user",
    parts=[
        Part.from_bytes(mime_type=mime_type, data=image_bytes),
        Part.from_text(text=user_question),
    ],
)

# 9) Llamar al modelo (usa uno de tu lista)
model_id = "gemini-2.5-flash"  # rápido y soporta imagen; en tu lista está habilitado

print("Diagnóstico rápido:")
print("  • Modelo:", model_id)
print("  • Imagen:", os.path.abspath(IMAGE_PATH))
print("  • MIME  :", mime_type)
print("  • Bytes :", len(image_bytes))

try:
    resp = client.models.generate_content(
        model=model_id,
        contents=contents
    )
except ClientError as e:
    print("\n❌ Error del cliente (ClientError):")
    print(e)
    print("\nSospechas y soluciones:")
    print("  1) Si dice NOT_FOUND: el modelo no coincide con tu lista. Usa exactamente uno de estos IDs:")
    print("     gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash, gemini-2.0-flash-001, gemini-2.0-flash-lite, etc.")
    print("  2) Si menciona v1beta: asegúrate de que el cliente tenga http_options={'api_version':'v1'}.")
    print("  3) Asegúrate de que .env tenga GOOGLE_API_KEY=... y que el venv esté activo.")
    sys.exit(1)

# 10) Imprimir respuesta
print("\n=== RESPUESTA MULTIMODAL ===")
print(getattr(resp, "text", str(resp)).strip())
