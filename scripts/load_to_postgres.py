import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        message_id BIGINT,
        channel_name VARCHAR,
        message_text TEXT,
        message_date TIMESTAMP,
        has_image BOOLEAN
    )
""")

for file in os.listdir('data/raw/telegram_messages'):
    with open(f'data/raw/telegram_messages/{file}', 'r') as f:
        for line in f:
            data = json.loads(line)
            cur.execute("""
                INSERT INTO raw.telegram_messages (message_id, channel_name, message_text, message_date, has_image)
                VALUES (%s, %s, %s, %s, %s)
            """, (data['id'], 'lobelia4cosmetics', data.get('message', ''), data['date'], bool(data.get('photo'))))
conn.commit()
cur.close()
conn.close()
