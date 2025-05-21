import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from app.handlers import router


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log'
    )
    logging.getLogger(__name__)
    asyncio.run(main())
