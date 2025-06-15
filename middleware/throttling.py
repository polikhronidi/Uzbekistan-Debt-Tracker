# middleware/throttling.py
import time
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_utils import get_user_lang
from locales import locales


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, minute_limit: int = 60, hour_limit: int = 150) -> None:
        super().__init__()
        self.minute_limit = minute_limit
        self.hour_limit = hour_limit
        self.storage: dict[int, dict] = {}

    async def on_process_message(self, message: types.Message, data: dict) -> None:
        await self._throttle(message.from_user.id, message.answer, message)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict) -> None:
        await self._throttle(call.from_user.id, call.answer, call)

    async def _throttle(self, user_id: int, responder, context) -> None:
        now = time.time()
        lang = get_user_lang(user_id)
        user = self.storage.setdefault(user_id, {"minute": [], "hour": [], "warned": False})

        # очистка старых меток
        user["minute"] = [t for t in user["minute"] if now - t < 60]
        user["hour"] = [t for t in user["hour"] if now - t < 3600]

        if len(user["minute"]) >= self.minute_limit or len(user["hour"]) >= self.hour_limit:
            if not user["warned"]:
                retry = self._get_retry_time(now, user, lang)
                await responder(f"{locales['too_many_requests'][lang]}\n\n{retry}",
                                show_alert=isinstance(context, types.CallbackQuery))
                user["warned"] = True
            raise CancelHandler()

        user["minute"].append(now)
        user["hour"].append(now)
        user["warned"] = False

    def _get_retry_time(self, now: float, user: dict, lang: str) -> str:
        if len(user["minute"]) >= self.minute_limit:
            sec = 60 - int(now - user["minute"][0])
            return locales["retry_seconds"][lang].format(sec)
        min_left = (3600 - int(now - user["hour"][0])) // 60
        return locales["retry_minutes"][lang].format(min_left)