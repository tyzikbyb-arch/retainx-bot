from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton

from keyboards import kb
from i18n import t
from database import get_lang

router = Router()

# ── Page builders ─────────────────────────────────────────────────────────────

def _back(lang: str, to: str) -> list:
    return [InlineKeyboardButton(text=t("btn_back", lang), callback_data=to)]


def _page_main(lang: str):
    return t("help_main_text", lang), kb(
        [InlineKeyboardButton(text=t("help_btn_start",  lang), callback_data="help_start")],
        [InlineKeyboardButton(text=t("help_btn_video",  lang), callback_data="help_video")],
        [InlineKeyboardButton(text=t("help_btn_images", lang), callback_data="help_images")],
        [InlineKeyboardButton(text=t("help_btn_audio",  lang), callback_data="help_audio")],
        [InlineKeyboardButton(text=t("help_btn_wallet", lang), callback_data="help_wallet")],
        [InlineKeyboardButton(text=t("help_btn_unlim",  lang), callback_data="help_unlim")],
        [InlineKeyboardButton(text=t("help_btn_ref",    lang), callback_data="help_ref")],
        [InlineKeyboardButton(text=t("help_btn_support",lang), callback_data="help_support")],
        _back(lang, "main_menu"),
    )


def _page_start(lang: str):
    return t("help_start_text", lang), kb(
        _back(lang, "help_main"),
    )


def _page_video(lang: str):
    return t("help_video_text", lang), kb(
        [InlineKeyboardButton(text=t("help_btn_vid_std",    lang), callback_data="help_vid_std")],
        [InlineKeyboardButton(text=t("help_btn_vid_prem",   lang), callback_data="help_vid_prem")],
        [InlineKeyboardButton(text=t("help_btn_vid_kling",  lang), callback_data="help_vid_kling")],
        [InlineKeyboardButton(text=t("help_btn_vid_avatar", lang), callback_data="help_vid_avatar")],
        _back(lang, "help_main"),
    )


def _page_vid_std(lang: str):
    return t("help_vid_std_text", lang), kb(
        _back(lang, "help_video"),
    )


def _page_vid_prem(lang: str):
    return t("help_vid_prem_text", lang), kb(
        _back(lang, "help_video"),
    )


def _page_vid_kling(lang: str):
    return t("help_vid_kling_text", lang), kb(
        _back(lang, "help_video"),
    )


def _page_vid_avatar(lang: str):
    return t("help_vid_avatar_text", lang), kb(
        _back(lang, "help_video"),
    )


def _page_images(lang: str):
    return t("help_images_text", lang), kb(
        _back(lang, "help_main"),
    )


def _page_audio(lang: str):
    return t("help_audio_text", lang), kb(
        _back(lang, "help_main"),
    )


def _page_wallet(lang: str):
    return t("help_wallet_text", lang), kb(
        [InlineKeyboardButton(text=t("help_btn_wallet_rates", lang), callback_data="help_wallet_rates")],
        [InlineKeyboardButton(text=t("help_btn_wallet_stars", lang), callback_data="help_wallet_stars")],
        [InlineKeyboardButton(text=t("help_btn_wallet_usdt",  lang), callback_data="help_wallet_usdt")],
        _back(lang, "help_main"),
    )


def _page_wallet_rates(lang: str):
    return t("help_wallet_rates_text", lang), kb(
        _back(lang, "help_wallet"),
    )


def _page_wallet_stars(lang: str):
    return t("help_wallet_stars_text", lang), kb(
        _back(lang, "help_wallet"),
    )


def _page_wallet_usdt(lang: str):
    return t("help_wallet_usdt_text", lang), kb(
        _back(lang, "help_wallet"),
    )


def _page_unlim(lang: str):
    return t("help_unlim_text", lang), kb(
        [InlineKeyboardButton(text=t("help_btn_unlim_std", lang), callback_data="help_unlim_std")],
        [InlineKeyboardButton(text=t("help_btn_unlim_pro", lang), callback_data="help_unlim_pro")],
        [InlineKeyboardButton(text=t("help_btn_unlim_vip", lang), callback_data="help_unlim_vip")],
        _back(lang, "help_main"),
    )


def _page_unlim_std(lang: str):
    return t("help_unlim_std_text", lang), kb(
        _back(lang, "help_unlim"),
    )


def _page_unlim_pro(lang: str):
    return t("help_unlim_pro_text", lang), kb(
        _back(lang, "help_unlim"),
    )


def _page_unlim_vip(lang: str):
    return t("help_unlim_vip_text", lang), kb(
        _back(lang, "help_unlim"),
    )


def _page_ref(lang: str):
    return t("help_ref_text", lang), kb(
        _back(lang, "help_main"),
    )


def _page_support(lang: str):
    return t("help_support_text", lang), kb(
        [InlineKeyboardButton(text=t("help_btn_support", lang), url="https://t.me/RetainXStudio")],
        _back(lang, "help_main"),
    )


_PAGES = {
    "help_main":         _page_main,
    "help_start":        _page_start,
    "help_video":        _page_video,
    "help_vid_std":      _page_vid_std,
    "help_vid_prem":     _page_vid_prem,
    "help_vid_kling":    _page_vid_kling,
    "help_vid_avatar":   _page_vid_avatar,
    "help_images":       _page_images,
    "help_audio":        _page_audio,
    "help_wallet":       _page_wallet,
    "help_wallet_rates": _page_wallet_rates,
    "help_wallet_stars": _page_wallet_stars,
    "help_wallet_usdt":  _page_wallet_usdt,
    "help_unlim":        _page_unlim,
    "help_unlim_std":    _page_unlim_std,
    "help_unlim_pro":    _page_unlim_pro,
    "help_unlim_vip":    _page_unlim_vip,
    "help_ref":          _page_ref,
    "help_support":      _page_support,
}


# ── Single handler dispatches all help_* callbacks ────────────────────────────

@router.callback_query(F.data.startswith("help_"))
async def help_dispatch(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    fn = _PAGES.get(cb.data)
    if not fn:
        await cb.answer()
        return
    text, kbd = fn(lang)
    await cb.answer()
    await cb.message.edit_text(text, reply_markup=kbd, parse_mode="HTML")
