import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import actions, aliases, models

API_TOKEN = os.environ["API_TOKEN"]

timeouts = {}
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

engine = create_engine("sqlite:///store/scb.db", echo=False)
session = sessionmaker(bind=engine)()
models.User.__table__.create(engine, checkfirst=True)


@dp.message_handler(content_types=[ContentType.STICKER])
async def handle_action(message) -> None:
    if message.content_type == "sticker":
        if message.sticker.file_unique_id == aliases.INCREASE_CREDIT_STICKER:
            await message.answer(
                actions.edit_social_credit(
                    message, session, aliases.Action.INCREASE, timeouts
                )
            )
        elif message.sticker.file_unique_id == aliases.DECREASE_CREDIT_STICKER:
            await message.answer(
                actions.edit_social_credit(
                    message, session, aliases.Action.DECREASE, timeouts
                )
            )


@dp.message_handler(commands=["social_rank"])
async def get_social_rank(message: types.Message):
    await message.reply(actions.get_report_of_social_rank(message, session))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
