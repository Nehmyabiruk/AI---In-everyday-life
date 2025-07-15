from fastapi import FastAPI
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )

@app.get("/messages")
async def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT channel_id, date_id, COUNT(*) as message_count
        FROM marts.fct_messages
        GROUP BY channel_id, date_id
    """)
    results = [{'channel_name': r[0], 'date': r[1], 'message_count': r[2]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@app.get("/products")
async def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.message_id, m.message_text, i.label, i.confidence
        FROM marts.fct_messages m
        JOIN raw.image_detections i ON m.message_id = i.message_id
    """)
    results = [{'message_id': r[0], 'message_text': r[1], 'product': r[2], 'confidence': r[3]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results
