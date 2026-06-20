from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def back_btn(callback: str, label: str = None, lang: str = "en") -> InlineKeyboardButton:
    if label is None:
        from i18n import t
        label = t("btn_back", lang)
    return InlineKeyboardButton(text=label, callback_data=callback)

def menu_btn(lang: str = "en") -> InlineKeyboardButton:
    from i18n import t
    return InlineKeyboardButton(text=t("menu_main_menu", lang), callback_data="main_menu")

def lang_btn(lang: str = "en") -> InlineKeyboardButton:
    from i18n import t
    return InlineKeyboardButton(text=t("btn_language", lang), callback_data="lang_menu")

def kb(*rows) -> InlineKeyboardMarkup:
    """Helper: pass lists of InlineKeyboardButton as positional args."""
    return InlineKeyboardMarkup(inline_keyboard=list(rows))

def kb_back_menu(back_cb: str) -> InlineKeyboardMarkup:
    return kb([back_btn(back_cb)], [menu_btn()])

def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def client_kb(lang: str = "en") -> ReplyKeyboardMarkup:
    from i18n import CLIENT_BUTTONS
    b = CLIENT_BUTTONS
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=b["main_menu"][lang]), KeyboardButton(text=b["wallet"][lang])],
            [KeyboardButton(text=b["video"][lang]), KeyboardButton(text=b["images"][lang]), KeyboardButton(text=b["audio"][lang])],
            [KeyboardButton(text=b["orders"][lang]), KeyboardButton(text=b["support"][lang])],
        ],
        resize_keyboard=True,
        persistent=True,
    )
