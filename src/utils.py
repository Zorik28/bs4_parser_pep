import logging

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import RequestException, Response
from requests_cache import CachedSession
from typing import Optional

from exceptions import ParserFindTagException


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
