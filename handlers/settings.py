# handlers/settings.py
from aiogram import types
from utils.db_utils import get_user_lang, conn
from locales import locales
from keyboards.inline import settings_menu, language_buttons


async def settings_handler(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await message.answer(locales["settings_menu"][lang], reply_markup=settings_menu(lang))


async def change_language(call: types.CallbackQuery) -> None:
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text(locales["language_prompt"][lang], reply_markup=language_buttons())


async def set_language(call: types.CallbackQuery) -> None:
    lang_code = call.data.split("_", 1)[1]
    user_id = call.from_user.id
    with conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (user_id, language_code) VALUES (?, ?)",
            (user_id, lang_code),
        )
    await call.message.edit_text(locales["language_saved"][lang_code])