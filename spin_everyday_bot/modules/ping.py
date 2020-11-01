#  SpinEverydayBot
#  Copyright © 2016-2017, 2020 Evgeniy Filimonov <evgfilim1@yandex.ru>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
from datetime import datetime

from aiogram import Router, Bot
from aiogram.api.types import Message
from ..db import User
from ..lang import tr as _

router = Router()


@router.message(commands=['ping'])
async def ping(message: Message):
    ping_time = (datetime.utcnow() - message.date.replace(tzinfo=None)).total_seconds()
    db_ping_t = datetime.utcnow()
    await User.get(1)
    db_ping = (datetime.utcnow() - db_ping_t).total_seconds()
    await message.reply(
        _('Pong!\nAnswer time: {0:.2f}s\nDatabase ping: {1:.2f}s').format(ping_time, db_ping)
    )
