from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


help_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/help')],
        [KeyboardButton(text='/notifications')],
        [KeyboardButton(text='/courses')],
        [KeyboardButton(text='/login')],
        [KeyboardButton(text='/logout')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Нажмите кнопку, чтобы получить список команд',
)
