import os
import json
from utils_db import get_db_conn

def lambda_handler(event, context):
    method = event.get('httpMethod')
    conn = get_db_conn()
    with conn.cursor() as cur:
        if method == 'GET':
            cur.execute("SELECT user_id, name, email FROM Users")
            rows = cur.fetchall()
            users = [{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows]
            return {'statusCode': 200, 'body': json.dumps(users)}

        if method == 'POST':
            data = json.loads(event.get('body', '{}'))
            cur.execute(
                "INSERT INTO Users(name, email) VALUES(%s,%s) RETURNING user_id",
                (data['name'], data['email'])
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            return {'statusCode': 201, 'body': json.dumps({'user_id': user_id})}

        if method == 'PUT':
            params = event.get('pathParameters') or {}
            uid = params.get('id')
            data = json.loads(event.get('body', '{}'))
            cur.execute(
                "UPDATE Users SET name=%s, email=%s WHERE user_id=%s",
                (data['name'], data['email'], uid)
            )
            conn.commit()
            return {'statusCode': 200, 'body': json.dumps({'updated': uid})}

    return {'statusCode': 400}