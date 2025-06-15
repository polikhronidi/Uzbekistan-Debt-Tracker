# main.py

import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup

from commands.set_bot_commands import set_bot_commands
from handlers.settings import settings_handler, change_language, set_language
from middleware.throttling import ThrottlingMiddleware
from utils.db_utils import conn, get_user_lang
from main_utils import (
    tashkent_now,
    build_chart,
    build_gif,
    get_last_known_update,
    save_last_update,
)
from locales import locales


TOKEN = "12345678910:AAAdisfsD9GAS80D712jgyOCSg09Fofvdg0iG9"
API_URL = (
    "http://api.worldbank.org/v2/country/uz/"
    "indicator/DT.DOD.DECT.CD?format=json&per_page=100"
)


def create_bot() -> Bot:
    return Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)


bot: Bot = create_bot()
dp: Dispatcher = Dispatcher(bot)
dp.middleware.setup(ThrottlingMiddleware())


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message) -> None:
    cur = conn.execute(
        "SELECT language_code FROM users WHERE user_id = ?", (message.from_user.id,)
    )
    row = cur.fetchone()
    if not row:
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.add(
            types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            types.InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
        )
        await message.answer(locales["language_prompt"]["ru"], reply_markup=kb)
        return

    lang = row[0]
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            locales["start_button"][lang], callback_data="get_debt"
        )
    )
    await message.answer(locales["start_message"][lang], reply_markup=kb)


@dp.message_handler(commands=["history"])
async def cmd_history(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    chart = await build_chart(lang)
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            locales["animate_button"][lang], callback_data="animate_debt"
        )
    )
    await message.answer_photo(
        InputFile(chart, filename="debt_chart.png"),
        caption=locales["gif_caption"][lang],
        reply_markup=kb,
    )


@dp.callback_query_handler(lambda c: c.data == "animate_debt")
async def cb_animate(callback: types.CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    # сразу отвечаем на клик, чтобы кнопка не висела в “часе ожидания”
    await callback.answer()
    await callback.message.answer(locales["animation_processing"][lang])
    gif = await build_gif(lang)
    await callback.message.answer_animation(
        InputFile(gif),
        caption=locales["gif_caption"][lang]
    )


@dp.message_handler(commands=["mydebt"])
async def cmd_mydebt(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    async with aiohttp.ClientSession() as sess:
        async with sess.get(API_URL) as resp:
            data = await resp.json()

    last = next(item["value"] for item in data[1] if item.get("value"))
    per_capita = last / 36_600_000
    if lang in ("ru", "uz"):
        formatted = f"{per_capita:,.2f}".replace(",", " ")
    else:
        formatted = f"{per_capita:,.2f}"

    await message.answer(
        locales["debt_per_capita"][lang].format(f"{formatted}$")
    )


@dp.message_handler(commands=["faq"])
async def cmd_faq(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await message.answer(locales["faq_text"][lang])


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await message.answer(locales["help_text"][lang])


@dp.message_handler(commands=["regions"])
async def cmd_regions(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    region_map = locales.get("regions_translations", {})
    if not region_map:
        return await message.answer(locales["region_in_progress"][lang])
    kb = InlineKeyboardMarkup(row_width=3)
    for region_key, names in region_map.items():
        label = names.get(lang, region_key)
        kb.insert(InlineKeyboardButton(label, callback_data=f"region_{region_key}"))
    await message.answer(locales["regions_rating"][lang], reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("region_"))
async def cb_region_detail(callback: types.CallbackQuery) -> None:
    region = callback.data.split("_", 1)[1]
    lang = get_user_lang(callback.from_user.id)
    name = locales["regions_translations"].get(region, {}).get(lang, region)
    await callback.message.answer(
        f"📍 <b>{name}</b>\n\n{locales['region_in_progress'][lang]}"
    )


@dp.callback_query_handler(lambda c: c.data == "get_debt")
async def cb_get_debt(callback: types.CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    async with aiohttp.ClientSession() as sess:
        async with sess.get(API_URL) as resp:
            data = await resp.json()

    last = next(item["value"] for item in data[1] if item.get("value"))
    if lang in ("ru", "uz"):
        fmt = f"{last:,.1f}".replace(".", ",")
    else:
        fmt = f"{last:,.1f}"

    text = locales["debt_info"][lang].format(tashkent_now(), f"{fmt}$")
    text += "\n" + locales["last_updated"][lang].format(
        data[0].get("lastupdated", "")
    )
    await callback.message.answer(text)


async def check_and_broadcast(bot_instance: Bot) -> None:
    async with aiohttp.ClientSession() as sess:
        async with sess.get(API_URL) as resp:
            data = await resp.json()

    current = data[0].get("lastupdated", "")
    last = get_last_known_update()
    if current and current != last:
        save_last_update(current)
        users = conn.execute(
            "SELECT user_id, language_code FROM users"
        ).fetchall()
        for uid, lang in users:
            kb = InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    locales["start_button"][lang], callback_data="get_debt"
                )
            )
            try:
                await bot_instance.send_message(
                    uid, locales["new_data_alert"][lang], reply_markup=kb
                )
            except Exception as e:
                logging.warning(f"Не удалось отправить {uid}: {e}")


async def scheduler(bot_instance: Bot) -> None:
    while True:
        await check_and_broadcast(bot_instance)
        await asyncio.sleep(3600)


if __name__ == "__main__":
    dp.register_message_handler(settings_handler, commands=["settings"])
    dp.register_callback_query_handler(change_language, text="change_lang")
    dp.register_callback_query_handler(set_language, text_startswith="lang_")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_commands(bot))
    loop.create_task(scheduler(bot))
    executor.start_polling(dp, skip_updates=False)