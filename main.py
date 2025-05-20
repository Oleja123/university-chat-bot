import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import Config


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()
storage = MemoryStorage


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log'
    )
    asyncio.run(main())
