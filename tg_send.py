import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import schedule
import time
import logging

# Logging sozlash
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API ma'lumotlari
API_ID = 10953300
API_HASH = '9c24426e5d6fa1d441913e3906627f87'
SESSION_STRING = '1BJWap1sBu2Y0X5ypRgA8WSq7pX81Fat6boZUtB1VezdbY7i6vOELTwTptq2QcpYx8o3c_aDnb7adWEl6SdzGlN1F7E6_jPZvJsoN53rqANWRMlsLohLVNir92sP8ZRKRLThi1q2Kl6tP2synXDV8dSnYOZVDHBVL7uSsFFYkF-GueDxOvZNzsj1exwJqW8b4jBt9v9FXZzKpWrKVnFy_cuRNAHU4-4M5sFfbz3LLq4aQFVSZtmtqerKUW3sKU64Jyj-8S9SUgTrP1hMt6qq7h0BHk0JjK5zKmoe-0PjbIWjJ7ic-XufImrhfdNTzQB2GYP-cur0gXT6MiXnGj0eYWIjkBKRRfTc='

# Forward qilinadigan xabar havolasi (siz bergan havolani shu yerga yozing)
MESSAGE_LINK = 'https://t.me/NeoSaleChat/108'  # O'z havolangizni qo'ying, masalan https://t.me/channel/123

# Client yaratish
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def get_all_groups():
    """Akkaunt qo'shilgan barcha guruhlarni olish"""
    groups = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            groups.append(dialog.id)
    return groups

async def send_scheduled_forward():
    """Belgilangan vaqtda xabarni forward qilish"""
    try:
        await client.start()
        # Havoladan entity va message_id olish
        entity, message_id = await client.resolve_url(MESSAGE_LINK)
        
        groups = await get_all_groups()
        if not groups:
            logging.error("Guruhlar topilmadi!")
            return

        for group_id in groups:
            try:
                await client.forward_messages(group_id, message_id, entity)
                logging.info(f"Xabar forward qilindi -> Guruh {group_id}")
            except Exception as e:
                logging.error(f"Guruh {group_id} ga forwardda xato: {e}")
                continue  # Xato bo'lsa, guruhni o'tkazib yuboramiz

        logging.info("Barcha forward tugadi!")
    except Exception as e:
        logging.error(f"Umumiy xato: {e}")
    finally:
        await client.disconnect()

def job():
    """Jadval uchun ish"""
    asyncio.run(send_scheduled_forward())

# Jadval: Har 6 soatda forward qilish
schedule.every(6).hours.do(job)

def run_scheduler():
    """Doimiy sikl"""
    logging.info("Dastur ishga tushdi!")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Har daqiqada tekshirish

if __name__ == "__main__":
    run_scheduler()