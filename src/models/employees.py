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

class Register(BaseModel):
    name: str = Form(..., title="Name", max_length=100)
    email: EmailStr = Form(..., title="Email")
    password: str = Form(..., title="Password", max_length=100, min_length=8)
    phone: str = Form(..., title="Phone No", max_length=50, pattern="^[0-9]{10}$")
    aadhaar: str = Form(..., title="Aadhaar No", max_length=50, pattern="^[0-9]{12}$")
    gender: Gender = Form()


class LoginModel(BaseModel):
    username: str
    password: str

class UpdateUserDetailsModel(BaseModel):
    name: str
    gender: int
    phone: str
    user_type: int

class ChangePasswordModel(BaseModel):
    new_password: str

class UpdateAddressModel(BaseModel):
    new_address: str

class UpdateProfilePicModel(BaseModel):
    filename: str

class JoinCompanyModel(BaseModel):
    organization: str
    position: str
    start_date: int
    comments: str
    is_verified: bool

class PromoteEmployeeModel(BaseModel):
    organization: str
    new_position: str
    date: int
    comments: str
    is_verified: bool

class EndEmploymentModel(BaseModel):
    organization: str
    date: int
    status: int
    comments: str
    is_verified: bool

class AddDocumentModel(BaseModel):
    document_type: int
    title: str
    document_id: str
    file_name: str
    file_url: str
    json_data: str
    verified_by: str
    date: int

class AddSkillModel(BaseModel):
    skill: str
    score: int
    verified_by: str
    date: int

class DisableAccessKeyModel(BaseModel):
    access_key: str

class FetchDocumentModel(BaseModel):
    document_type: str
    district: str = None
    passing_year: str = None
    panno: str = None
    roll_number: str = None