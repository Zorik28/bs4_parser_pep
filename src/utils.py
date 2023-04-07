import logging
from enum import Enum
from pathlib import Path
from typing import Optional, Callable

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import RequestException, Response
from requests_cache import CachedSession

from exceptions import NoneResponseException, ParserFindTagException


def get_response(session: CachedSession, url: str) -> Response:
    """GET-response with the RequestException trapping."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            # function call stack display
            stack_info=True
        )


def is_none(
        func: Callable[[CachedSession, str], Response]
) -> Callable[[CachedSession, str], Response]:
    """Checks if response is None"""
    if func is None:
        error_msg = 'Нет контента на странице. Проверьте url в запросе!'
        logging.error(error_msg, stack_info=True)
        raise NoneResponseException(error_msg)
    return func


def mkdir_and_path(path: Path, directory: str, filename: str) -> Path:
    """Creats a directory and return the path, and also catches the erorrs."""
    try:
        path_dir = path / directory
        path_dir.mkdir(exist_ok=True)
        return path_dir / filename
    except OSError:
        logging.exception(
            f'Возникла ошибка при создании папки {directory}',
            stack_info=True
        )


def find_tag(
        soup: BeautifulSoup, tag: str, attrs: Optional[dict] = None
) -> Tag:
    """BeautifulSoup.find() method with an erorr trapping."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def enum_values(cls: Enum) -> tuple:
    """Gets a tuple of values within enum class."""
    return tuple([item.value for item in cls])
