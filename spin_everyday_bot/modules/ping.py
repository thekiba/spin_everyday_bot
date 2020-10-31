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

from ..lang import tr as _

router = Router()


@router.message(commands=['ping'])
async def ping(message: Message, bot: Bot):
    ping_time = (datetime.utcnow() - message.date.replace(tzinfo=None)).total_seconds()
    m = await message.reply(_('Pong!\nAnswer time: {0:.2f}').format(ping_time))
    ping_time = (datetime.utcnow() - m.date.replace(tzinfo=None)).total_seconds()
    await bot.edit_message_text(m.text + _('\nTelegram ping time: {0:.2f}').format(ping_time),
                                message_id=m.message_id, chat_id=m.chat.id)
