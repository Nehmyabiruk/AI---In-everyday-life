import os
import logging
from datetime import datetime
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='scrape.log', level=logging.INFO)

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
channel = 'lobelia4cosmetics'

async def main():
    async with TelegramClient('session', api_id, api_hash) as client:
        date_str = datetime.now().strftime('%Y-%m-%d')
        os.makedirs(f'data/raw/telegram_messages/{date_str}', exist_ok=True)
        async for message in client.iter_messages(channel, limit=50):
            with open(f'data/raw/telegram_messages/{date_str}/{channel}.json', 'a') as f:
                f.write(str(message.to_dict()) + '\n')
            if message.photo:
                os.makedirs(f'data/raw/telegram_images/{date_str}/{channel}', exist_ok=True)
                await message.download_media(f'data/raw/telegram_images/{date_str}/{channel}/')
            logging.info(f'Scraped message {message.id} from {channel}')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
