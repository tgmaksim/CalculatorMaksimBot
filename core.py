OWNER = 5128609241
NAME = "CalculatorMaksimBot"
SITE = "https://tgmaksim.ru/проекты/калькулятор"
subscribe = "https://t.me/+AypnXcgxrHE3YTk6"
channel = "@MaksimMyBots"

markdown = "Markdown"
html = "HTML"


import sys_keys
import aiosqlite
import traceback
from typing import Union
from datetime import datetime, timedelta
from aiogram.types import Message, CallbackQuery


class db:
    db_path = "db.sqlite3"

    @staticmethod
    async def execute(sql: str, params: tuple = tuple()) -> tuple[tuple[str]]:
        async with aiosqlite.connect(resources_path(db.db_path)) as conn:
            async with conn.execute(sql, params) as cur:
                result = await cur.fetchall()
            await conn.commit()
        return result


def security(*arguments):
    def new_decorator(fun):
        async def new(_object: Union[Message, CallbackQuery], **kwargs):
            try:
                await fun(_object, **{kw: kwargs[kw] for kw in kwargs if kw in arguments})
            except Exception as e:
                exception = "".join(traceback.format_exception(e))
                await _object.bot.send_message(OWNER, f"⚠️Ошибка⚠️\n\n{exception}")

        return new

    return new_decorator


def resources_path(path: str) -> str:
    return sys_keys.resources_path(path, NAME)


def time_now() -> datetime:
    return datetime.utcnow() + timedelta(hours=6)


def omsk_time(t: datetime):
    tz = int(t.tzinfo.utcoffset(None).total_seconds() // 3600)
    return (t + timedelta(hours=6-tz)).replace(tzinfo=None)


async def get_users() -> set:
    return set(map(lambda x: int(x[0]), await db.execute("SELECT id FROM users")))


async def get_version():
    return (await db.execute("SELECT value FROM system_data WHERE key=?", ("version",)))[0][0]


async def set_version(version):
    await db.execute("UPDATE system_data SET value=? WHERE key=?", (version, "version"))