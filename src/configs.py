import logging

from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from typing import Iterable

from constants import DT_FORMAT, LOG_DIR, LOG_FILE, LOG_FORMAT
from enums.modes import additional_modes


def configure_argument_parser(available_modes: Iterable) -> ArgumentParser:
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
    LOG_DIR.mkdir(exist_ok=True)
    # Инициализация хендлера с ротацией логов.
    # Максимальный объём одного файла — 1МБ,
    # максимальное количество файлов с логами — 5.
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10**6, backupCount=5
    )
    # Базовая настройка логирования basicConfig.
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        # Уровень записи логов.
        level=logging.INFO,
        # Вывод логов в терминал.
        handlers=(rotating_handler, logging.StreamHandler())
    )
