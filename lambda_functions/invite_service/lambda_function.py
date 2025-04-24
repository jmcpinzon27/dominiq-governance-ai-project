import os
import json
import uuid
from urllib.parse import quote_plus
from utils_db import get_db_conn
from email_sender import send_invite_email

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    users = body.get('users', [])  # Lista de dicts con keys 'id' y 'email'

    conn = get_db_conn()
    with conn.cursor() as cur:
        for u in users:
            token = str(uuid.uuid4())
            cur.execute(
                "UPDATE Users SET invite_token=%s WHERE user_id=%s",
                (token, u['id'])
            )
            link = f"https://<TU_FRONT>/app?invite={quote_plus(token)}"
            send_invite_email(u['email'], link)
        conn.commit()

    return {'statusCode': 200, 'body': json.dumps({'status': 'invites_sent'})}