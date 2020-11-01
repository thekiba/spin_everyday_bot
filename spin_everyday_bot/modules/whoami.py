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
from html import escape

from aiogram import Router
from aiogram.api.types import Message
from ..db import user_ctx, chat_ctx, chat_user_ctx

router = Router()


@router.message(commands=['whoami'])
async def whoami(message: Message):
    user = user_ctx.get()
    chat = chat_ctx.get()
    chat_user = chat_user_ctx.get()
    await message.reply(f"You are {escape(repr(user.full_name))!r} in chat {escape(repr(chat))}"
                        f" (extra={escape(repr(chat_user))})")