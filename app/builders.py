from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


async def inline_notifications(data):
    keyboard = InlineKeyboardBuilder()
    for notification in data['items']:
        keyboard.add(InlineKeyboardButton(
            text=f"{notification.message} {'✅' if notification.has_read else ''}",
            callback_data=f"notification:{notification.id}",
        ))

    page = data['_meta']['page']
    total_pages = data['_meta']['total_pages']
    total_items = data['_meta']['total_items']

    if total_items == 0:
        return None

    left = page-1 if page != 1 else total_pages
    right = page+1 if page != total_pages else 1

    left_button = InlineKeyboardButton(
        text="←", callback_data=f"notifications:{left}")
    page_button = InlineKeyboardButton(
        text=f"{data['_meta']['page']}/{data['_meta']['total_pages']}", callback_data="None")
    right_button = InlineKeyboardButton(
        text="→", callback_data=f"notifications:{right}")
    keyboard.adjust(1)
    keyboard.row(left_button, page_button, right_button)
    return keyboard.as_markup()


async def inline_notification(data):
    keyboard = InlineKeyboardBuilder()

    if not data.has_read:
        read_button = InlineKeyboardButton(
            text="Прочитать", callback_data=f"read_notification:{data.id}")
        keyboard.add(read_button)
    delete_button = InlineKeyboardButton(
        text="Удалить", callback_data=f"delete_notification:{data.id}")
    keyboard.add(delete_button)
    keyboard.adjust(1)
    return keyboard.as_markup()


async def inline_courses(data):
    keyboard = InlineKeyboardBuilder()
    for course in data['items']:
        keyboard.add(InlineKeyboardButton(
            text=f"{course.course_name} {'✅' if course.date_completion else ''}",
            callback_data=f"course:{course.teacher_id}:{course.course_id}",
        ))

    page = data['_meta']['page']
    total_pages = data['_meta']['total_pages']
    total_items = data['_meta']['total_items']

    if total_items == 0:
        return None

    left = page-1 if page != 1 else total_pages
    right = page+1 if page != total_pages else 1

    left_button = InlineKeyboardButton(
        text="←", callback_data=f"courses:{left}")
    page_button = InlineKeyboardButton(
        text=f"{data['_meta']['page']}/{data['_meta']['total_pages']}", callback_data="None")
    right_button = InlineKeyboardButton(
        text="→", callback_data=f"courses:{right}")
    keyboard.adjust(1)
    keyboard.row(left_button, page_button, right_button)
    return keyboard.as_markup()


async def inline_course(data):
    keyboard = InlineKeyboardBuilder()

    if data.sertificate_loaded:
        download_button = InlineKeyboardButton(
            text="Скачать сертификат", callback_data=f"download_sertificate:{data.teacher_id}:{data.course_id}")
        keyboard.add(download_button)
    return keyboard.as_markup()
