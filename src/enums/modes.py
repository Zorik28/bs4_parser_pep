from enum import Enum

from utils import enum_values


class AdditionalMode(str, Enum):
    PRETTY = 'pretty'
    FILE = 'file'

    @classmethod
    @property
    def to_display(cls):
        """Returns 'pretty' and 'file' modes"""
        return enum_values(cls)
