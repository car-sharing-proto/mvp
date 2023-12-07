from enum import Enum


class Role(str, Enum):
    Admin   = 'admin'
    User    = 'user'