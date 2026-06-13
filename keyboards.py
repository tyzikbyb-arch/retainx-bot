from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_btn(callback: str, label: str = "← Back") -> InlineKeyboardButton:
    return InlineKeyboardButton(text=label, callback_data=callback)

def menu_btn() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="⌂  Main Menu", callback_data="main_menu")

def kb(*rows) -> InlineKeyboardMarkup:
    """Helper: pass lists of InlineKeyboardButton as positional args."""
    return InlineKeyboardMarkup(inline_keyboard=list(rows))

def kb_back_menu(back_cb: str) -> InlineKeyboardMarkup:
    return kb([back_btn(back_cb)], [menu_btn()])

def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]
