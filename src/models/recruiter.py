from src.models._base import *

class hcOutput(hcSuccessModal):
    data: dict = Body()

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

class Register(BaseModel):
    organization: str = Form(..., title="Organization Name", max_length=100)
    email: EmailStr = Form(..., title="Email")
    password: str = Form(..., title="Password", max_length=100, min_length=8)
    phone: str = Form(..., title="Phone No", max_length=50, pattern="^[0-9]{10}$")
