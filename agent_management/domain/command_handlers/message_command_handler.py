import uuid


# from domain.command.message_command import GetMessages, GetListMessages, ListMessages, Message
# from domain.command.registration_command import GetRegistrations, Registrations
from domain.command.comon_command import Sources


async def get_message(sources: Sources, data): #GetMessages):
    pass
    # params = []
    # data.email and params.append({"attr": "email", "op": "eq", "value": data.email})
    # data.session_id and params.append({"attr": "session_id", "op": "eq", "value": data.session_id})
    # params = GetListMessages(params=params)
    # list_message:ListMessages = await sources.nosql.messages.get_list_mesasge_by_attrs(params)
    # api_response = await sources.asistant.send_message_to_asistant(list_message)
    # if api_response:
    #     registration_ref: Registrations = await sources.nosql.registrations.get_registration_by_attrs(
    #         GetRegistrations(email=data.email or list_message.root[0].email)
    #     )
    #     list_message.root.append(Message(**{
    #         "role": "assistant", 
    #         "email": data.email or list_message.root[0].email,
    #         "session_id": data.session_id or list_message.root[0].session_id,
    #         "content": f"Hola {registration_ref.responsible},"
    #             " gusto en saludarte. Has sido registrado como responsable del"
    #             f" subdominio {registration_ref.subdomain} perteneciente al"
    #             f" dominio {registration_ref.domain} en la industria "
    #             f"{registration_ref.industry}. Mi objetivo es ayudarte a "
    #             "conceptualizar tu área/subdominio específico."
    #     }))
    #     return list_message


async def get_generate_diagram_from_cha(sources: Sources, data): # GetMessages):
    pass
    # list_messages = sources.nosql.message.get_message_by_attrs(GetMessages)
    # mermaid_code = sources.asistant.get_generate_diagram_from_asistant(list_messages)
    # diagram_id = str(uuid.uuid4())
    # file_name = f"diagram_{diagram_id}.html"
    # html_content = f"""
    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <meta charset="UTF-8">
    #     <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.3/mermaid.min.js"></script>
    # </head>
    # <body>
    #     <div class="mermaid">{mermaid_code}</div>
    #     <script>mermaid.initialize({{ startOnLoad: true }});</script>
    # </body>
    # </html>
    # """
    # diagram_url = sources.storage.upload_content_to_storage(html_content, diagram_id)
    # return {"diagram_url": diagram_url}