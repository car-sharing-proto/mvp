from enum import Enum


class UserResponse(str, Enum):
    AlreadyExists           = 'user with this ID already exists'
    NotFound                = 'user not found'
    SuccessfullyAdded       = 'user is successfully added'
    SuccessfullyUpdated     = 'user is successfully updated'
    SuccessfullyRemoved     = 'user is successfully removed'