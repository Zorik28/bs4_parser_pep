import logging

from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from typing import Iterable

from constants import DT_FORMAT, LOG_DIR, LOG_FILE, LOG_FORMAT
from enums.modes import additional_modes


def configure_argument_parser(available_modes: Iterable) -> ArgumentParser:
    """Set up the argument parser."""
    parser = ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=additional_modes,
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging() -> None:
    """Set up the logging. Handler initialization with log rotation.
    The max size of file is 1MB, the max number of files with logs is 5."""
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10**6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        # Output logs to the stream.
        handlers=(rotating_handler, logging.StreamHandler())
    )
