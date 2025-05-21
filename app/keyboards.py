from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


login_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(
        text='Войти', 
        callback_data='login',
    )]],
    resize_keyboard=True,
    input_field_placeholder='Нажмите на кнопку входа',
)
