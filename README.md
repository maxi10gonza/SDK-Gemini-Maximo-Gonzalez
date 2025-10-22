# SDK Gemini – Máximo González

## Requisitos
- Una **API Key** de **Google AI Studio**

## Obtener API Key (Google AI Studio)
1. Ve a: https://aistudio.google.com/app/apikey  
2. Crea una API key y cópiala.
3. En la carpeta del proyecto, crea **`.env`** con:

GOOGLE_API_KEY=AIza...tu_clave...

## Entorno virtual
py -m venv .venv
.venv\Scripts\Activate

## Paquetes
python -m pip install --upgrade pip
pip install --upgrade google-genai python-dotenv

### Ver Modelos disponibles
Usa uno de estos IDs (según tu cuenta). Ejemplo de salida real:

```bash
models/gemini-2.5-flash
models/gemini-2.5-pro
models/gemini-2.0-flash
```
### Comando
```bash
python -c "import os; from dotenv import load_dotenv; from google import genai; load_dotenv(); c=genai.Client(api_key=os.getenv('GOOGLE_API_KEY'), http_options={'api_version':'v1'}); print(*[m.name for m in c.models.list()], sep='\n')"
```
### Archivo: act3_generate_content.py
Ejecutar:
```bash
python act3_generate_content.py
```
### Archivo: act4_generate_content_stream.py
Ejecutar:
```bash
python act4_generate_content_stream.py
```
### Archivo: act5_multimodal_image.py
Crear carpeta y poner imagen:
```bash
mkdir assets
# Copia tu imagen a .\assets\ (por ejemplo, foto_comida.jpg)
python act5_multimodal_image.py
```

