from aiogram import Dispatcher, Bot
from .cli import init_parser, parse_args
from .lang import tr as _
from .config import config_ctx, Settings


def main():
    args = parse_args(init_parser())
    if args.fetch_type == 'webhook':
        raise NotImplementedError(_('Getting updates via webhook is not implemented yet'))
    settings = Settings()
    config_ctx.set(settings)

    bot = Bot(settings.token, parse_mode='HTML')
    dp = Dispatcher()
    dp.run_polling(bot)
