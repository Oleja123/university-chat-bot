from functools import wraps
import logging

from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.builders import inline_notifications
from app.exceptions.non_authorized_error import NonAuthorizedError
from app.keyboards import login_kb
from app.services import auth_service, notification_service


router = Router()
user_tokens = {}
logger = logging.getLogger(__name__)

class Login(StatesGroup):
    username = State()
    password = State()


def token_check(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        try:
            if args[0].from_user.id not in user_tokens:
                raise NonAuthorizedError
            return await f(*args, **kwargs)
        except NonAuthorizedError:
            return await args[0].answer('Ошибка авторизации: введите команду /login, чтобы авторизоваться')
    return decorated_function


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
    except ValueError as e:
        await message.answer(f"Ошибка при авторизации: {e}")
    except Exception as e:
        await message.answer(f"Неизвестная ошибка")
    await state.clear()


@router.message(Command('logout'))
async def logout(message: Message):
    user_id = message.from_user.id
    if user_id not in user_tokens:
        await message.answer('Вы не авторизованы')
    else:
        del user_tokens[message.from_user.id]
        await message.answer('Вы успешно вышли из аккаунта')


async def get_notifications(user_id, page=1):
    notifications = notification_service.get_all_paginated(
        int(user_tokens[user_id]['id']),
        user_tokens[user_id]['token'],
        page=page
    )
    logger.info(notifications)
    return await inline_notifications(notifications)


@router.message(Command('notifications'))
@token_check
async def notifications(message: Message):
    user_id = message.from_user.id
    await message.reply('Список твоих уведомлений:',
                        reply_markup=await get_notifications(user_id))


@router.callback_query(lambda c: c.data and c.data.startswith('notifications:'))
@token_check
async def notifiactions_callback(callback: CallbackQuery):
    page = int(callback.data.split(':')[-1])
    user_id = callback.from_user.id
    await callback.answer()
    return callback.message.edit_reply_markup(reply_markup=await get_notifications(user_id, page))
