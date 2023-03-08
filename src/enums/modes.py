from enum import Enum


class AdditionalMode(Enum):
    PRETTY = 'pretty'
    FILE = 'file'

    @classmethod
    @property
    def to_display(cls):
        return tuple(cls._value2member_map_)
