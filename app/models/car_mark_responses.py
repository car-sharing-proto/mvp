from enum import Enum


class CarMarkResponse(str, Enum):
    AlreadyExists           = 'car mark with this ID already exists'
    NotFound                = 'car mark not found'
    SuccessfullyAdded       = 'car mark is successfully added'
    SuccessfullyUpdated     = 'car mark is successfully updated'
    SuccessfullyRemoved     = 'car mark is successfully removed'