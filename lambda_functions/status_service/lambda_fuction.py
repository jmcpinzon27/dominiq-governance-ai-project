import os
import json
from utils_db import get_db_conn

def lambda_handler(event, context):
    conn = get_db_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM Session WHERE completed = TRUE")
        completed = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Session WHERE completed = FALSE")
        open_sessions = cur.fetchone()[0]

    return {
        'statusCode': 200,
        'body': json.dumps({
            'completed_sessions': completed,
            'open_sessions': open_sessions
        })
    }