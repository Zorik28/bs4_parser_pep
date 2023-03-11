from enum import Enum


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
        return tuple([item.value for item in cls][:3])

    @classmethod
    @property
    def status_quantity(cls) -> tuple:
        return tuple([item.value for item in cls][:3])
