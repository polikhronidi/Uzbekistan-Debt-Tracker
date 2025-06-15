# commands/set_bot_commands.py
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

COMMANDS = {
    "ru": [
        ("start", "🚀 Начать работу с ботом"),
        ("history", "📈 График роста госдолга"),
        ("mydebt", "💰 Ваш долг на душу населения"),
        ("faq", "📚 Что такое госдолг?"),
        ("regions", "🌍 Рейтинг по регионам"),
        ("help", "🆘 Подсказки и справка"),
    ],
    "en": [
        ("start", "🚀 Start working with the bot"),
        ("history", "📈 Debt growth chart"),
        ("mydebt", "💰 Your per capita debt"),
        ("faq", "📚 What is national debt?"),
        ("regions", "🌍 Regional debt ranking"),
        ("help", "🆘 Help and info"),
    ],
    "uz": [
        ("start", "🚀 Bot bilan ishlashni boshlash"),
        ("history", "📈 Qarz o‘sish grafigi"),
        ("mydebt", "💰 Aholi boshiga qarz"),
        ("faq", "📚 Davlat qarzi nima?"),
        ("regions", "🌍 Hududlar reytingi"),
        ("help", "🆘 Yordam va ma’lumot"),
    ],
}


async def set_bot_commands(bot: Bot) -> None:
    for lang, items in COMMANDS.items():
        cmds = [BotCommand(name, desc) for name, desc in items]
        await bot.set_my_commands(cmds, scope=BotCommandScopeDefault(), language_code=lang)