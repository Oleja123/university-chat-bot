from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keybords import login_kb
from app.services import auth_service


router = Router()
user_tokens = {}


class Login(StatesGroup):
    username = State()
    password = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear() 
    await message.reply(f"Привет\nТвой id: {message.from_user.id}\n",
                        reply_markup=login_kb)


@router.message(Command('login'))
async def enter_username(message: Message, state: FSMContext):
    await state.set_state(Login.username)
    await message.answer('Введите имя пользователя')


@router.message(Login.username)
async def enter_username_inter(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Login.password)
    await message.answer('Введите пароль')


@router.message(Login.password)
async def enter_password_inter(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    try:
        data = await state.get_data()
        res = auth_service.login(data['username'], data['password'])
        user_tokens[message.from_user.id] = res
        await state.update_data(token=res)
        await message.answer(f"Ваш токен: {res['token']}")
    except Exception as e:
        await message.answer(f"Ошибка при авторизации: {e}")
    await state.clear()


@router.message(Command('logout'))
async def logout(message: Message):
    user_id = message.from_user.id
    if user_id not in user_tokens:
        await message.answer('Вы не авторизованы')
    else:
        del user_tokens[message.from_user.id]
        await message.answer('Вы успешно вышли из аккаунта')
