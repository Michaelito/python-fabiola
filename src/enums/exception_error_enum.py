from enum import Enum


class ExceptionErrorEnum(Enum):
    OK = 0
    DATA_NOT_FOUND = -1
    UNAUTHORIZED = -2
    INVALID_PASSWORD = -3
    UNKNOWN_ERROR = -999
