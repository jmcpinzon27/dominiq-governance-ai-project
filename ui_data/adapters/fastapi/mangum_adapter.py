import json
import uuid
import requests
from flask_cors import CORS
from google.cloud import firestore, storage

from fastapi import FastAPI

from mangum import Mangum

app = FastAPI()


# Configuración de CORS para permitir todas las solicitudes
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Agregar encabezados CORS manualmente en todas las respuestas
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Manejar solicitudes OPTIONS (preflight) antes de las peticiones POST
@app.before_request
def handle_preflight(request):
    if request.method == "OPTIONS":
        response = {"message": "Solicitud preflight,K"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

# Configuración de la API externa
API_URL = "https://api.saia.ai/chat"
AUTH_TOKEN = "default_QJ6z12CWdeLnW3uKOag7xUUkzmwOC8vQk161eAJyV4NT4ozBkZyruWW9XdJqxuNKqjTVLcnS3EWt7QF9qff_C0t0-JkoevWcaOmVpzwgq6E968Dg6HfDZWEWWorsaO4j_fgC_gV3GNM3_qXgDuKr7jUbeE7xu8va9BeTlVA-Lb4="

# Inicializar Firestore y Cloud Storage
db = firestore.Client()
storage_client = storage.Client()
BUCKET_NAME = "html-buckets"  # Reemplaza con el nombre real del bucket en GCP

def upload_html_to_gcs(html_content, file_name):
    """Sube un archivo HTML a Google Cloud Storage y devuelve su URL pública."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.upload_from_string(html_content, content_type="text/html")
    blob.make_public()
    return blob.public_url

@app.route('/get_user_data', methods=['GET'])
def get_user_data(request):
    """Obtiene los datos del usuario basados en el email."""
    email = request.args.get('email')
    if not email:
        return {"error": "Debes proporcionar un email."}, 400

    try:
        registration_ref = db.collection('registrations').where('email', '==', email).get()
        if not registration_ref:
            return {"error": "No se encontró el usuario."}, 404

        registration_data = registration_ref[0].to_dict()
        return registration_data, 200
    except Exception as e:
        return {"error": f"Ha ocurrido un error: {str(e)}"}, 500

@app.route('/chat_with_agent', methods=['POST'])
def chat_with_agent(request):
    """Maneja el diálogo con el agente IA."""
    try:
        request_json = request.get_json()
        if not request_json or "id" not in request_json:
            return {"error": "Debes proporcionar un identificador de sesión ('id')."}, 400

        session_id = request_json["id"]
        doc_ref = db.collection('chat_sessions').document(session_id)
        doc = doc_ref.get()
        messages = doc.to_dict().get("messages", []) if doc.exists else []

        if "message" in request_json:
            user_message = request_json["message"]
            messages.append({"role": "user", "content": user_message})
        else:
            return {"error": "Debes enviar un mensaje válido en el cuerpo de la solicitud."}, 400

        # Recuperar información del registro si el email está presente
        

        # Crear el payload para la API externa
        payload = {
            "model": "saia:assistant:dominiQ-Assistant",
            "messages": messages
        }

        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            api_response = response.json()
            assistant_message = api_response["choices"][0]["message"]
            registration_ref = db.collection('registrations').where('email', '==', request_json["email"]).get()
            registration_data = registration_ref[0].to_dict()
            messages.append({"role": "assistant", "content": assistant_message["content"] + f"Hola {registration_data['responsible']}, gusto en saludarte. Has sido registrado como responsable del subdominio {registration_data['subdomain']} perteneciente al dominio {registration_data['domain']} en la industria {registration_data['industry']}. Mi objetivo es ayudarte a conceptualizar tu área/subdominio específico."})
            doc_ref.set({"messages": messages})
            return api_response , 200
        else:
            return {"error": "Error en la API externa", "details": response.text}, 500

    except Exception as e:
        return {"error": f"Ha ocurrido un error: {str(e)}"}, 500

@app.route('/generate_diagram_from_chat', methods=['POST'])
def generate_diagram_from_chat(request):
    """Genera un diagrama a partir del historial de chat y lo almacena en GCS."""
    try:
        request_json = request.get_json()
        if not request_json or "id" not in request_json:
            return {"error": "Debes proporcionar un identificador de sesión ('id')."}, 400

        session_id = request_json["id"]
        doc_ref = db.collection('chat_sessions').document(session_id)
        doc = doc_ref.get()
        if not doc.exists:
            return {"error": "No se encontró historial para esta sesión."}, 404

        messages = doc.to_dict().get("messages", [])
        summary_payload = {
            "model": "saia:assistant:summary assistant",
            "messages": [{"role": "system", "content": "Resume la siguiente conversación de manera clara y concisa."}] + messages
        }

        headers = {"Authorization": f"Bearer {AUTH_TOKEN}", "Content-Type": "application/json"}
        summary_response = requests.post(API_URL, headers=headers, json=summary_payload)
        if summary_response.status_code != 200:
            return {"error": "Error en la API de resumen"}, 500

        summary_text = summary_response.json()["choices"][0]["message"]["content"]
        flowchart_payload = {
            "model": "saia:assistant:DominiQ-summaryToFormat",
            "messages": [
                {"role": "system", "content": "Convierte el siguiente resumen en un formato de diagrama de flujo en Mermaid.js. Devuelve SOLO el código Mermaid, sin texto adicional."},
                {"role": "user", "content": summary_text}
            ]
        }

        flowchart_response = requests.post(API_URL, headers=headers, json=flowchart_payload)
        if flowchart_response.status_code != 200:
            return {"error": "Error en la API de conversión"}, 500

        mermaid_code = flowchart_response.json()["choices"][0]["message"]["content"]
        mermaid_code = mermaid_code.replace('```mermaid', '').replace('```', '').strip()
        diagram_id = str(uuid.uuid4())
        file_name = f"diagram_{diagram_id}.html"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.3/mermaid.min.js"></script>
        </head>
        <body>
            <div class="mermaid">{mermaid_code}</div>
            <script>mermaid.initialize({{ startOnLoad: true }});</script>
        </body>
        </html>
        """

        diagram_url = upload_html_to_gcs(html_content, file_name)
        return {"diagram_url": diagram_url}, 200

    except Exception as e:
        return {"error": f"Error: {str(e)}"}, 500


if __name__ == 'main':
    handler = Mangum(app)
