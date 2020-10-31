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
