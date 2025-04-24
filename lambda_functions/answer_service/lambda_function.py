import os
import json
from utils_db import get_db_conn

def lambda_handler(event, context):
    data = json.loads(event.get('body', '{}'))
    user_id = data.get('user_id')
    question_id = data.get('question_id')
    answer = data.get('answer')
    is_last = data.get('is_last', False)

    conn = get_db_conn()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO MaturityAnswers(user_id, question_id, answer_text, is_last_question) VALUES (%s,%s,%s,%s)",
            (user_id, question_id, answer, is_last)
        )
        # Opcional: lógica cuando is_last=True (marcar sesión completa)
        conn.commit()

    return {'statusCode': 200, 'body': json.dumps({'status': 'saved'})}