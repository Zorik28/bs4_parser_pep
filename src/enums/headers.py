from enum import Enum


class Header(Enum):
    ARTICLE_LINK = 'Ссылка на статью'
    HEADER = 'Заголовок'
    EDITOR = 'Редактор, Автор'
    STATUS = 'Status'
    QUANTITY = 'Quantity'

    @classmethod
    @property
    def first_row(cls):
        return tuple(cls._value2member_map_)[:3]

    @classmethod
    @property
    def status_quantity(cls):
        return tuple(cls._value2member_map_)[3:]
