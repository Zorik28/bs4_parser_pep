from enum import Enum


class Choice(Enum):
    PRETTY = 'pretty'
    FILE = 'file'

    @staticmethod
    def additional_modes():
        return tuple(Choice._value2member_map_)


additional_modes = Choice.additional_modes()
