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

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from dataclasses import dataclass
from typing import Type, Optional, Sequence

from .lang import tr as _


@dataclass()
class Args:
    fetch_type: str
    host: str
    port: int


def init_parser() -> ArgumentParser:
    parser = ArgumentParser(description=_('Telegram bot for everyday drawings'),
                            formatter_class=ArgumentDefaultsHelpFormatter)
    run_type = parser.add_subparsers(
        title='fetch type',
        help=_('How to fetch updates, see https://core.telegram.org/bots/api#getting-updates'),
        dest='fetch_type'
    )
    run_type.add_parser('polling', help=_('Run with polling (default)'))
    webhook = run_type.add_parser('webhook', help=_('Run with webhooks (not supported yet)'))
    webhook.add_argument('--host', '-h', help=_('Host to listen at'))
    webhook.add_argument('--port', '-p', type=int, help=_('Port to listen at'))

    return parser


def parse_args(
        parser: ArgumentParser,
        args_cls: Type[Args] = Args,
        argv: Optional[Sequence[str]] = None
) -> Args:
    args = parser.parse_args(argv)
    return args_cls(**args.__dict__)


__all__ = ('parse_args', 'init_parser', 'Args')
