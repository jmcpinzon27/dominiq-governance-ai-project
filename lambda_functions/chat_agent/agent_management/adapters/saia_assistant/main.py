import logging

import httpx

# from domain.command.message_command import ListMessages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "https://api.saia.ai/chat"
AUTH_TOKEN = "default_QJ6z12CWdeLnW3uKOag7xUUkzmwOC8vQk161eAJyV4NT4ozBkZyruWW9XdJqxuNKqjTVLcnS3EWt7QF9qff_C0t0-JkoevWcaOmVpzwgq6E968Dg6HfDZWEWWorsaO4j_fgC_gV3GNM3_qXgDuKr7jUbeE7xu8va9BeTlVA-Lb4="


async def send_message_to_asistant(messages):# ListMessages):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {AUTH_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "saia:assistant:dominiQ-Assistant",
                    "messages": messages.model_dump(mode='json')
                }
            )

        if response.status_code == 200:
            api_response = response.json()
            return api_response["choices"][0]["message"]
        else:
            logger.error(f"Error en la API externa", "details {response.text}")
    except Exception as err:
        logger.error("Error sisa: %s", err)


async def get_generate_diagram_from_asistants(messages):
    summary_payload = {
        "model": "saia:assistant:summary assistant",
        "messages": [{"role": "system", "content": "Resume la siguiente conversación de manera clara y concisa."}] + messages
    }

    headers = {"Authorization": f"Bearer {AUTH_TOKEN}",
               "Content-Type": "application/json"}
    summary_response = await httpx.post(API_URL, headers=headers, json=summary_payload)
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

    flowchart_response = await httpx.post(API_URL, headers=headers, json=flowchart_payload)
    if flowchart_response.status_code != 200:
        return {"error": "Error en la API de conversión"}, 500

    mermaid_code = flowchart_response.json(
    )["choices"][0]["message"]["content"]
    return mermaid_code.replace('```mermaid', '').replace('```', '').strip()
