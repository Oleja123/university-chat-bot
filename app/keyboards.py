from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


login_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(
        text='/help', 
    )]],
    resize_keyboard=True,
    input_field_placeholder='Нажмите кнопку, чтобы получить список команд',
)
