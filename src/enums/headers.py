from enum import Enum

from constants import LINK_HEADER_EDITOR, STATUS_QUANTITY
from utils import enum_values


class Header(Enum):
    ARTICLE_LINK = 'Ссылка на статью'
    HEADER = 'Заголовок'
    EDITOR = 'Редактор, Автор'
    STATUS = 'Status'
    QUANTITY = 'Quantity'

    @classmethod
    @property
    def first_row(cls) -> tuple:
        """Returns the headers"""
        return enum_values(cls)[:LINK_HEADER_EDITOR]

    @classmethod
    @property
    def status_quantity(cls) -> tuple:
        return enum_values(cls)[STATUS_QUANTITY:]
