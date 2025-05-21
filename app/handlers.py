from mailbox import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart

from app.keybords import login_kb


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"Привет\nТвой id: {message.from_user.id}\n",
                        reply_markup=login_kb)