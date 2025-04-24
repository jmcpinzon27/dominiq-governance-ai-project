from datetime import datetime
import json
import pickle
import requests
import random
import time

import streamlit as st

from domain.command_handlers.maturity_question_handler import LoaderFactory
from domain.command.maturity_question_command import ChatResponse


HEADERS = {
    "Authorization": "Bearer default_QJ6z12CWdeLnW3uKOag7xUUkzmwOC8vQk161eAJyV4NT4ozBkZyruWW9XdJqxuNKqjTVLcnS3EWt7QF9qff_C0t0-JkoevWcaOmVpzwgq6E968Dg6HfDZWEWWorsaO4j_fgC_gV3GNM3_qXgDuKr7jUbeE7xu8va9BeTlVA-Lb4=",
    "Content-Type": "application/json"
} 


# Streamed response emulator. Not used
def response_generator_basic(input):
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    # return response
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


@st.cache_data
def ini_prompt(jsonstring):
    # url = 'https://api.beta.saia.ai/chat/completions'
    # url='https://api.agentx.globant.com/chat/completions'
    url='https://api.saia.ai/v1/assistant/c50d9071-ad56-488d-bbe4-303edc9faad7' #[DominiQ], 8cf95f45-539f-4444-9fff-97e206a86e23

    data = {
        # "model": "saia:assistant:[DominiQ] Data Maturity Survey", #[DominiQ] Data Maturity Survey
        "action": "save", #savePublishNewRevision. Save updates the specified revision ID
        "revisionId": 4,
        "prompt": jsonstring,
        "llmSettings":{
          "modelName":"gpt-4o-mini",
          "temperature":0.0
        }
       
    }
    response = requests.put(url, headers=HEADERS, json=data)
    # print(response)
    # j = response.json() 
    return response


@st.cache_data
def response_generator(jsonstring):
    # url = 'https://api.beta.saia.ai/chat/completions'
    # url='https://api.agentx.globant.com/chat/completions'
    url='https://api.saia.ai/chat/completions'

    headers = {**HEADERS, "saia-conversation-id": "user1"}
 
    data = {
        "model": "saia:assistant:[DominiQ]Maturity", #[DominiQ] Data Maturity Survey
        "revision": 4,
        "messages": [
            {
                "role": "user",
                "content": jsonstring
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    # print(response)
    j = response.json() 
    return j['choices'][0]['message']['content']


@st.cache_data
def format_generator(jsonstring):
    # url = 'https://api.beta.saia.ai/chat/completions'
    # url='https://api.agentx.globant.com/chat/completions'
    url='https://api.saia.ai/chat/completions'

    headers = {**HEADERS, "saia-conversation-id": "user1"}
 
    data = {
        "model": "saia:assistant:[DominiQ]Maturity_format", #[DominiQ] Data Maturity Survey
        "revision": 1,
        "messages": [
            {
                "role": "user",
                "content": jsonstring
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    # print(response)
    j = response.json() 
    return j['choices'][0]['message']['content']


userID="AAA"


def init_asistant(questions):

    st.title("Dominique")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'res' not in st.session_state:
        st.session_state.res="No question yet"


    # if st.button("Update questions"):
    # json_loader = LoaderFactory.create_loader("xlsx", "[Template] Deep Survey - Data Maturity.xlsx")
    # questions = json_loader.load_questions(sort_by_category=True)
    apiQResponse=''.join(str(x) for x in questions)

    promt_questions=f"""Tu eres un asistente encargado de realizar una encuesta para Globant. Preséntate al usuario nada más iniciar la conversación y vete formulando las preguntas una a una. 

    QUESTIONS = {apiQResponse}

    Tendrás que completar, con las respuestas del usuario,  todas las preguntas que están en QUESTIONS.
    Para cada pregunta, muestra las posibles opciones de respuesta. La respuesta tiene que siempre tener el numero de la opción. Siendo 1 el valor más bajo de options. Ejemplo:
    1: Not evaluated
    2: Null
    3: Muy baja
    4: Baja
    5: Media
    6: Alta

    Devuelve simplemente preguntas de QUESTIONS hasta finalizar el cuestionario. 

    Consideraciones adicionales:

    - Serás amable y  comentaras entre preguntas para hacer una charla amena, almacenando las respuestas.
    - Enumera las preguntas faltantes. ej:(1/10)"""
    
    st.write("Ini assistant:", ini_prompt(promt_questions))
    st.write("Questions file updated")


    # Display chat messages from history on app rerun
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])


    # st.write(st.session_state.messages)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def ask_question(input_text: str, questions, file_content: str):
    init_asistant(questions)
    try:
        if file_content:
            session_data = pickle.loads(file_content)
            st.session_state.messages = session_data.get("messages", [])
            st.session_state.res = session_data.get("res", "No question yet")
        
        with st.chat_message("user"):
            st.markdown(input_text)
            st.session_state.messages.append(
                {"role": "user", "content": input_text}
            )
            
            # Format and save response
            # json_to_save = format_generator({
            #     "userID": userID,
            #     "datetime": datetime.today().strftime('%Y-%m-%d_%H%M%S'),
            #     "pregunta_aisstente": st.session_state.res,
            #     "respuesta_usuario": input_text
            # })
            
            # if "<JSONRETURN>" in json_to_save:
            #     solution = find_between(json_to_save, "<JSONRETURN>", "</JSONRETURN>")
            #     filename = f'answers_user1.json'
            #     with open(filename, 'a+', encoding='utf-8') as f:
            #         json.dump(json.loads(solution), f, indent=4, ensure_ascii=False)

        # Generate assistant response
        with st.chat_message("assistant"):
            st.session_state.res = response_generator(st.session_state.messages)
            st.write(st.session_state.res)
            st.session_state.messages.append({
                "role": "assistant", "content": st.session_state.res
            })
        
        byte_data = pickle.dumps(st.session_state.messages)
        return byte_data, ChatResponse(
            messages=st.session_state.messages[-1],
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        pass
        # raise HTTPException(status_code=500, detail=str(e))
