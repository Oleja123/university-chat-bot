from functools import wraps
import logging

from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.builders import inline_notification, inline_notifications
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
        except Exception as e:
            return await args[0].answer(str(e))
    return decorated_function


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(f"Привет\nТвой id: {message.from_user.id}\n",
                        reply_markup=login_kb)


@router.message(Command('login'))
async def enter_username(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Login.username)
    await message.answer('Введите имя пользователя')


@router.message(Command('logout'))
async def logout(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if user_id not in user_tokens:
        await message.answer('Вы не авторизованы')
    else:
        del user_tokens[message.from_user.id]
        await message.answer('Вы успешно вышли из аккаунта')


@router.message(Command('notifications'))
@token_check
async def notifications(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    res = await get_notifications(user_id)
    if res:
        await message.reply(text='Список ваших уведомлений:', reply_markup=res)
    else:
        await message.reply(text='Уведомлений нет', reply_markup=None)


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


async def get_notifications(user_id, page=1):
    notifications = notification_service.get_all_paginated(
        int(user_tokens[user_id]['id']),
        user_tokens[user_id]['token'],
        page=page
    )
    logger.info(notifications)
    return await inline_notifications(notifications)


@router.callback_query(lambda c: c.data and c.data.startswith('notifications:'))
@token_check
async def notifiactions_callback(callback: CallbackQuery):
    page = int(callback.data.split(':')[-1])
    user_id = callback.from_user.id
    await callback.answer()
    res = await get_notifications(user_id, page)
    if res:
        await callback.message.edit_text(text='Список ваших уведомлений:', reply_markup=res)
    else:
        await callback.message.edit_text(text='Уведомлений нет', reply_markup=None)


@router.callback_query(lambda c: c.data and c.data.startswith('notification:'))
@token_check
async def notifiaction_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    notification = notification_service.get_by_id(int(callback.data.split(':')[-1]),
                                                  user_tokens[user_id]['token'])
    await callback.answer()
    await callback.message.edit_text(text=notification.__repr__() + " \nВсе уведомления /notifications",
                                     reply_markup=await inline_notification(notification))


@router.callback_query(lambda c: c.data and c.data.startswith('read_notification:'))
@token_check
async def notifiaction_read_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    notification = notification_service.read(int(callback.data.split(':')[-1]),
                                             user_tokens[user_id]['token'])
    await callback.answer()
    await callback.message.edit_text(text=notification.__repr__() + " \nВсе уведомления /notifications",
                                     reply_markup=await inline_notification(notification))


@router.callback_query(lambda c: c.data and c.data.startswith('delete_notification:'))
@token_check
async def notifiaction_delete_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    notification_service.delete_notification(int(callback.data.split(':')[-1]),
                                             user_tokens[user_id]['token'])
    await callback.answer()
    await callback.message.edit_text(text='Уведомление успешно удалено\nВсе уведомления /notifications',
                                     reply_markup=None)
