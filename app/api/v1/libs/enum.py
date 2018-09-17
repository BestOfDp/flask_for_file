from enum import Enum


class AuthEnum(Enum):
    ORDINARY = 0
    ADMIN = 1
    SUPER = 2


class SaveFileEnum(Enum):
    IMAGE = 1
    FILE = 2


class FilePublicAuthEnum(Enum):
    PUBLIC = 1
    PRIVATE = 2
    DELETED = 3


class StatusEnum(Enum):
    DELETE = 0
    NORMAL = 1
