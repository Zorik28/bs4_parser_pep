from enum import Enum


class AdditionalMode(Enum):
    PRETTY = 'pretty'
    FILE = 'file'

    @classmethod
    @property
    def to_display(cls):
        """Returns 'pretty' and 'file' modes"""
        return tuple([item.value for item in cls])
