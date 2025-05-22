from functools import wraps
import logging

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.builders import inline_course, inline_courses, inline_notification, inline_notifications
from app.exceptions.non_authorized_error import NonAuthorizedError
from app.keyboards import help_kb
from app.services import auth_service, notification_service, teacher_course_service


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
        except NonAuthorizedError as e:
            logger.error(e)
            return await args[0].answer('Ошибка авторизации: введите команду /login, чтобы авторизоваться')
        except Exception as e:
            logger.error(e)
            return await args[0].answer(str(e))
    return decorated_function


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(f"Привет\nОтправь команду /help, чтобы получить список команд\n",
                        reply_markup=help_kb)
    

@router.message(Command('help'))
async def help(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Login.username)
    await message.answer('Список команд\n' + \
                         '/help - помощь\n' + \
                         '/notifications - список уведомлений\n' + \
                         '/courses - список курсов\n' + \
                         '/login - вход в аккаунт\n' + \
                         '/logout - выход из аккаунта\n')



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


@router.message(Command('courses'))
@token_check
async def courses(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    res = await get_courses(user_id)
    if res:
        await message.reply(text='Список ваших курсов:', reply_markup=res)
    else:
        await message.reply(text='У вас нет курсов', reply_markup=None)


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
async def notification_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    notification = notification_service.get_by_id(int(callback.data.split(':')[-1]),
                                                  user_tokens[user_id]['token'])
    await callback.answer()
    await callback.message.edit_text(text=notification.__repr__() + " \nВсе уведомления /notifications",
                                     reply_markup=await inline_notification(notification))


@router.callback_query(lambda c: c.data and c.data.startswith('read_notification:'))
@token_check
async def notification_read_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    notification = notification_service.read(int(callback.data.split(':')[-1]),
                                             user_tokens[user_id]['token'])
    await callback.answer()
    await callback.message.edit_text(text=notification.__repr__() + " \nВсе уведомления /notifications",
                                     reply_markup=await inline_notification(notification))


@router.callback_query(lambda c: c.data and c.data.startswith('delete_notification:'))
@token_check
async def notification_delete_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    notification_service.delete_notification(int(callback.data.split(':')[-1]),
                                             user_tokens[user_id]['token'])
    await callback.answer()
    await callback.message.edit_text(text='Уведомление успешно удалено\nВсе уведомления /notifications',
                                     reply_markup=None)


async def get_courses(user_id, page=1):
    courses = teacher_course_service.get_all_paginated(
        int(user_tokens[user_id]['id']),
        user_tokens[user_id]['token'],
        page=page
    )
    logger.info(courses)
    return await inline_courses(courses)


@router.callback_query(lambda c: c.data and c.data.startswith('courses:'))
@token_check
async def courses_callback(callback: CallbackQuery):
    page = int(callback.data.split(':')[-1])
    user_id = callback.from_user.id
    await callback.answer()
    res = await get_courses(user_id, page)
    if res:
        await callback.message.edit_text(text='Список ваших курсов:', reply_markup=res)
    else:
        await callback.message.edit_text(text='У вас нет курсов', reply_markup=None)


@router.callback_query(lambda c: c.data and c.data.startswith('course:'))
@token_check
async def course_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    course = teacher_course_service.get_by_ids(int(callback.data.split(':')[-2]),
                                               int(callback.data.split(
                                                   ':')[-1]),
                                               user_tokens[user_id]['token'])
    await callback.answer()
    await callback.message.edit_text(text=course.__repr__() + " \nВсе курсы /courses",
                                     reply_markup=await inline_course(course))


@router.callback_query(lambda c: c.data and c.data.startswith('download_sertificate:'))
@token_check
async def download_sertificate_callback(callback: CallbackQuery):
    user_id = int(callback.data.split(':')[-2])
    course_id = int(callback.data.split(':')[-1])
    f = teacher_course_service.download_teacher_course(
        user_id, course_id, user_tokens[callback.from_user.id]['token'])
    await callback.answer()
    await callback.message.answer_document(
        document=FSInputFile(f.name, filename=f'Сертификат {user_id}:{course_id}'),
        caption='Сертификат успешно отправлен'
    )
