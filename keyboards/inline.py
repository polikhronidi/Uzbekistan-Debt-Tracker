# keyboards/inline.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from locales import locales


def settings_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(locales["choose_lang_btn"][lang], callback_data="change_lang")
    )


def language_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
    )