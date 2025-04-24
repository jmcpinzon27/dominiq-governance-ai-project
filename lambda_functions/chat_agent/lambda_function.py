import os, json
from utils_db import get_db_conn
from openai_client import ask_agent

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    user_id   = payload['user_id']
    question  = payload.get('message')

    conn = get_db_conn()
    # recupera next_question de la BD, etc…
    agent_reply = ask_agent(question, user_id, conn)

    # persiste respuesta
    with conn.cursor() as cur:
        cur.execute(
           "INSERT INTO MaturityAnswers(user_id, question_id, answer_text) VALUES (%s,%s,%s)",
           (user_id, payload['question_id'], agent_reply)
        )
        conn.commit()

    return {
      "statusCode": 200,
      "body": json.dumps({"reply": agent_reply})
    }
