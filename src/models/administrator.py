from src.models._base import *


class Gender(int, Enum):
    Male = 0
    Female = 1
    Other = 2

class UserType(int, Enum):
    Admin = 0
    Organization = 1
    Employee = 2

class UserStatus(int, Enum):
    Registered = 0
    Approved = 1
    Deactivated = 2
