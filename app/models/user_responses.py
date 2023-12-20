from enum import Enum


class UserResponse(str, Enum):
    AlreadyExists           = 'user with this ID already exists'
    SuccessfullyAdded       = 'user is successfully added'
    SuccessfullyUpdated     = 'user is successfully updated'