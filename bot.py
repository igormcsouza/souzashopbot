from datetime import datetime
import os
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, executor, types
from sqlmodel import SQLModel, Field, select
from sqlmodel.engine.create import create_engine
from sqlmodel.orm.session import Session

from utils import Converters, process_text

API_TOKEN = os.environ['TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO, filename="bot.log")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class ShopList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantite: float
    item: str
    whom: str
    timestamp: Optional[float] = Converters.datetime2timestamp(datetime.now())
    checked: Optional[bool] = False


engine = create_engine("sqlite:///db.sqlite")

if not os.path.isfile("db.sqlite"):
    SQLModel.metadata.create_all(engine)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("Hello! I'm going to help with the shop list!")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """
    await message.reply(
        """It's simple to use, send /add, enter, and the shop list (quantite-item).
        For example:
        /add
        2-carrots
        1-ice cream""")


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    items = process_text(message.text)
    with Session(engine) as session:
        for quantite, item in items:
            item = ShopList(quantite=quantite,
                            item=item,
                            whom=message.from_user.first_name)
            session.add(item)

        session.commit()

    await message.answer("Added to the list!")


def postprocess_rows(row: ShopList):
    return f"Buy {row.quantite} of {row.item} - Added {Converters.timestamp2datetime(row.timestamp)} by {row.whom}.\n"  # noqa: E501


@dp.message_handler(commands=['shop'])
async def shop(message: types.Message):
    query = select(ShopList).where(ShopList.checked == False)  # noqa: E712

    with Session(engine) as session:
        results = session.exec(query)

        shoplist = list(map(postprocess_rows, results))

    with Session(engine) as session:
        results = session.exec(query)

        for each in results:
            each.checked = True
            session.add(each)

        session.commit()

    if len(shoplist) == 0:
        await message.answer("No items on the shop list!! :D")
    else:
        await message.answer("".join(shoplist))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
