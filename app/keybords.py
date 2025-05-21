from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


login_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Войти')]],
    resize_keyboard=True,
    input_field_placeholder='Нажмите на кнопку входа'
)
