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

from aiogram import Dispatcher, Bot
from spin_everyday_bot.cli import init_parser, parse_args
from spin_everyday_bot.config import config_ctx, Settings
from spin_everyday_bot.lang import tr as _
from spin_everyday_bot.modules import router as modules


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args(init_parser())
    if args.fetch_type == 'webhook':
        raise NotImplementedError(_('Getting updates via webhook is not implemented yet'))
    settings = Settings()
    config_ctx.set(settings)

    bot = Bot(settings.token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(modules)
    dp.run_polling(bot)


main()
