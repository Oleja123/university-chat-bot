from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


async def inline_notifications(data):
    keyboard = InlineKeyboardBuilder()
    for notification in data['items']:
        keyboard.add(InlineKeyboardButton(
            text=notification.message,
            callback_data=f"notification:{notification.id}",
        ))
    
    page = data['_meta']['page']
    total_pages = data['_meta']['total_pages']

    left  = page-1 if page != 1 else total_pages
    right = page+1 if page != total_pages else 1

    left_button  = InlineKeyboardButton(text="←", callback_data=f"notifications:{left}")
    page_button  = InlineKeyboardButton(text=f"{data['_meta']['page']}/{data['_meta']['total_pages']}", callback_data="None") 
    right_button = InlineKeyboardButton(text="→", callback_data=f"notifications:{right}")
    keyboard.adjust(1)
    keyboard.row(left_button, page_button, right_button)
    return keyboard.as_markup()
