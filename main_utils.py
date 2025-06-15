# main_utils.py  (вынес утилиты из main.py)
import io
import json
from datetime import datetime
from pathlib import Path

import aiohttp
import matplotlib.pyplot as plt
import numpy as np
import pytz
from PIL import Image

from locales import locales
import matplotlib as mpl
API_URL = "http://api.worldbank.org/v2/country/uz/indicator/DT.DOD.DECT.CD?format=json&per_page=100"
LAST_UPDATE_FILE = Path("last_updated.json")

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = [
    'DejaVu Sans',
    'Noto Color Emoji',
    'EmojiOne Color',
]

def tashkent_now() -> str:
    return datetime.now(pytz.timezone("Asia/Tashkent")).strftime("%Y-%m-%d %H:%M:%S")


def get_last_known_update() -> str:
    if LAST_UPDATE_FILE.exists():
        return json.loads(LAST_UPDATE_FILE.read_text()).get("last", "")
    return ""


def save_last_update(date: str) -> None:
    LAST_UPDATE_FILE.write_text(json.dumps({"last": date}))


async def fetch_debt_data() -> list[tuple[int, float]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            data = await resp.json()
    return sorted(
        (int(item["date"]), item["value"]) for item in data[1] if item.get("value") is not None
    )


async def build_chart(lang: str) -> io.BytesIO:
    data = await fetch_debt_data()
    years, vals = zip(*data)
    vals = [v / 1e9 for v in vals]

    labels = {
        "title": {"ru": "📊 Рост госдолга Узбекистана", "en": "📊 Growth of Uzbekistan's Debt", "uz": "📊 O'zbekiston davlat qarzi"},
        "x": {"ru": "Год", "en": "Year", "uz": "Yil"},
        "y": {"ru": "Долг (млрд $)", "en": "Debt (billion $)", "uz": "Qarz (mlrd $)"},
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(years, vals, marker="o", linewidth=2)
    ax.set_title(labels["title"][lang], fontsize=16, fontweight="bold")
    ax.set_xlabel(labels["x"][lang])
    ax.set_ylabel(labels["y"][lang])
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xticks(np.arange(min(years), max(years) + 1, 2))
    ax.tick_params(axis="x", rotation=45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for x, y in zip(years[-5:], vals[-5:]):
        ax.text(x, y + max(vals) * 0.01, f"{y:.1f}", ha="center", fontsize=9)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


async def build_gif(lang: str) -> io.BytesIO:
    data = await fetch_debt_data()
    years, vals = zip(*data)
    vals = [v / 1e9 for v in vals]

    frames = []
    for i in range(1, len(years) + 1):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(years[:i], vals[:i], marker="o", linewidth=2)
        ax.set_title({"ru": "Рост госдолга Узбекистана", "en": "Uzbekistan Debt Growth", "uz": "O'zbekiston qarz o‘sishi"}[lang], fontsize=14, fontweight="bold")
        ax.set_xlim(min(years), max(years))
        ax.set_ylim(0, max(vals) * 1.1)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        buf_img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf_img, format="png")
        plt.close(fig)
        buf_img.seek(0)
        frames.append(Image.open(buf_img).convert("P"))

    gif_buf = io.BytesIO()
    frames[0].save(gif_buf, format="GIF", save_all=True, append_images=frames[1:], duration=300, loop=0)
    gif_buf.name = "debt_growth.gif"
    gif_buf.seek(0)
    return gif_buf