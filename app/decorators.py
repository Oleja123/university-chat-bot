from functools import wraps

from aiogram.types import Message

from app.exceptions.non_authorized_error import NonAuthorizedError


async def token_check(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        try:
            await f(args, kwargs)
        except NonAuthorizedError:
            await kwargs['message'].answer('Введите пароль')
        return f(*args, **kwargs)
    return decorated_function