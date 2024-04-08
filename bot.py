"""Launches the bot"""

import os
import subprocess
from asyncio import run
from typing import Union
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import Config, load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.callbacks import register_callbacks
from tgbot.handlers.commands import register_commands
from tgbot.handlers.errors import register_errors
from tgbot.handlers.messages import register_messages
from tgbot.middlewares.localization import i18n
from tgbot.misc.commands import set_default_commands
from tgbot.misc.logger import logger
from tgbot.services.database import database


def register_all_middlewares(dp: Dispatcher) -> None:
    """Registers middlewares"""
    dp.middleware.setup(i18n)


def register_all_filters(dp: Dispatcher) -> None:
    """Registers filters"""
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher) -> None:
    """Registers handlers"""
    register_admin(dp)
    register_commands(dp)
    register_messages(dp)
    register_callbacks(dp)
    register_errors(dp)


async def start_bot() -> None:
    """Starts the bot"""
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())
    bot["config"] = config

    try:
        register_all_middlewares(dp)
        register_all_filters(dp)
        register_all_handlers(dp)
        await database.init()
        await set_default_commands(dp)
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


def start_web_server() -> None:
    """Starts the web server in the background"""
    command = ["python", "simple_server.py"]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd=os.getcwd())


if __name__ == "__main__":
    logger.info("Starting bot")
    try:
        start_web_server()
        run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as ex:
        logger.critical("Unknown error: %s", repr(ex))
    logger.info("Bot stopped!")
