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
import logging
from typing import Any, Callable, Awaitable, TypeVar

from gino.crud import UpdateRequest

from aiogram import Router
from aiogram.api.types import InlineQuery, ChosenInlineResult, Message, CallbackQuery
from ..db import User, Chat, ChatUser, user_ctx, chat_ctx, chat_user_ctx

router = Router()
logger = logging.getLogger(__name__)

_RT = TypeVar('_RT')
_UET = TypeVar('_UET', Message, InlineQuery, ChosenInlineResult, CallbackQuery)
_CET = TypeVar('_CET', Message, CallbackQuery)


@router.message.outer_middleware()
@router.edited_message.outer_middleware()
@router.inline_query.outer_middleware()
@router.chosen_inline_result.outer_middleware()
@router.callback_query.outer_middleware()
async def user_middleware(
        handler: Callable[[_UET, dict[str, Any]], Awaitable[_RT]],
        event: _UET,
        data: dict[str, Any],
) -> _RT:
    tg_user = event.from_user
    user = await User.query.where(User.tg_id == event.from_user.id).gino.one_or_none()
    create = user is None
    if create:
        user = User(tg_id=tg_user.id, username=tg_user.username, full_name=tg_user.full_name)
        await user.create()
        # data['user'] = user
        user_ctx.set(user)
        return await handler(event, data)
    # logger.debug('Found existing user')
    update = user
    if user.username != tg_user.username:
        update = update.update(username=tg_user.username)
    if user.full_name != tg_user.full_name:
        update = update.update(full_name=tg_user.full_name)
    if isinstance(update, UpdateRequest):
        await update.apply()
    # data['user'] = user
    user_ctx.set(user)
    return await handler(event, data)


@router.message.outer_middleware()  # need to check before chat_user_middleware
async def migrate_middleware(
        handler: Callable[[Message, dict[str, Any]], Awaitable[_RT]],
        message: Message,
        data: dict[str, Any],
) -> _RT:
    if (migrate := message.migrate_from_chat_id) is not None:
        chat = await Chat.query.where(Chat.tg_id == migrate)
        if chat is not None:
            await chat.update(tg_id=message.chat.id).apply()
    return await handler(message, data)


@router.message.outer_middleware()
@router.edited_message.outer_middleware()
@router.callback_query.outer_middleware()
async def chat_user_middleware(
        handler: Callable[[_CET, dict[str, Any]], Awaitable[_RT]],
        event: _CET,
        data: dict[str, Any],
) -> _RT:
    if isinstance(event, CallbackQuery):
        if event.message is None:
            # data['chat'] = None
            # data['chat_user'] = None
            # chat_ctx.set(None)
            # chat_user_ctx.set(None)
            return await handler(event, data)  # nothing to do
        msg: Message = event.message
    else:
        msg: Message = event
    if msg.chat.type == 'private':
        # data['chat'] = None
        # data['chat_user'] = None
        # chat_ctx.set(None)
        # chat_user_ctx.set(None)
        return await handler(event, data)
    tg_chat = msg.chat
    chat = await Chat.query.where(Chat.tg_id == tg_chat.id).gino.one_or_none()
    if chat is None:
        chat = Chat(tg_id=tg_chat.id)
        await chat.create()
    # data['chat'] = chat
    chat_ctx.set(chat)
    # user: User = data['user']
    user = user_ctx.get()
    if user is None:
        logger.error('user_ctx is empty!')
        return await handler(event, data)
    chat_user = await ChatUser.query\
        .where((ChatUser.user_id == user.id) & (ChatUser.chat_id == chat.id))\
        .gino.one_or_none()
    if chat_user is None:
        chat_user = ChatUser(user_id=user.id, chat_id=chat.id)
        await chat_user.create()
    # data['chat_user'] = chat_user
    chat_user_ctx.set(chat_user)
    return await handler(event, data)
