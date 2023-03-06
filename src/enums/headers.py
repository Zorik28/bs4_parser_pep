from enum import Enum


class Header(Enum):
    ARTICLE_LINK = 'Ссылка на статью'
    HEADER = 'Заголовок'
    EDITOR = 'Редактор, Автор'
    STATUS = 'Status'
    QUANTITY = 'Quantity'

    @staticmethod
    def first_row():
        return tuple(Header._value2member_map_)


first_row = Header.first_row()[:3]
status_quantity = Header.first_row()[3:]
