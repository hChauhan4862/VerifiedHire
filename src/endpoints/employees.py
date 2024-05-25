from src.endpoints._base import *
from src.models.employees import *
from uuid import uuid4
import requests
import random
from utils.third_party.aadhaar import demographic_auth
from utils.third_party.hs_api import UPBOARD_HS_MARKSHEET_API
from utils.third_party.ss_api import UPBOARD_SS_MARKSHEET_API

#APIRouter creates path operations for item module
router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.post("/signup")
async def register(r: Register):
    if blockchain.functions.doesUserExist(r.email).call():
        raise hcCustomException(detail="User already exists")
    
    G = "M" if r.gender == 0 else ("F" if r.gender == 1 else "O")

    a = demographic_auth(r.aadhaar, r.name, G)
    if a["error"] != "success":
        raise hcCustomException(detail=a["error"])

    a = blockChainTransact(blockchain.functions.registerUser(
        r.name,
        r.email,
        r.gender,
        r.phone,
        UserType.Employee,  # Assuming 2 is the user type for employee
        r.password
    ))

    blockChainTransact(blockchain.functions.activateUser(r.email, "Automatic By System", "System"))

    return hcRes(detail="Registration successful")
    

@router.post("/login")
async def login(response: Response, username: str = Body(), password: str = Body()):
    session = uuid4()
    a = blockChainTransact(blockchain.functions.login(username, password, str(session), UserType.Employee))
    EmployeeCookie.attach_to_response(response, session)
    return hcRes(detail="Login successful")
    

@router.post("/logout")
async def logout(response: Response, session_id: UUID = Depends(EmployeeCookie)):
    EmployeeCookie.delete_from_response(response)
    blockchain.functions.logout(str(session_id)).call()
    return hcRes(detail="Logout successful")

@router.get("/whoami", dependencies=[Depends(EmployeeCookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getAdminProfile(session_data.username).call())

@router.post("/updateUserDetails", dependencies=[Depends(EmployeeCookie)])
async def update_user_details(email: str, name: str, gender: int, phone: str, user_type: int, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateUserDetails(email, name, gender, phone, user_type))
    return hcRes(detail="User details updated successfully")

@router.post("/changePassword", dependencies=[Depends(EmployeeCookie)])
async def change_password(email: str, new_password: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.changePassword(email, new_password))
    return hcRes(detail="Password changed successfully")

@router.get("/getStatusHistory", dependencies=[Depends(EmployeeCookie)])
async def get_status_history(email: str):
    return hcRes(data=blockchain.functions.getStatusHistory(email).call())

@router.post("/updateAddress", dependencies=[Depends(EmployeeCookie)])
async def update_address(email: str, new_address: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateAddress(email, new_address))
    return hcRes(detail="Address updated successfully")

@router.get("/getCurrentAddress", dependencies=[Depends(EmployeeCookie)])
async def get_current_address(email: str):
    return hcRes(data=blockchain.functions.getCurrentAddress(email).call())

@router.post("/updateProfilePic", dependencies=[Depends(EmployeeCookie)])
async def update_profile_pic(email: str, filename: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateProfilePic(email, filename))
    return hcRes(detail="Profile picture updated successfully")

@router.get("/getProfilePic", dependencies=[Depends(EmployeeCookie)])
async def get_profile_pic(email: str):
    return hcRes(data=blockchain.functions.getProfilePic(email).call())

@router.post("/joinCompany", dependencies=[Depends(EmployeeCookie)])
async def join_company(email: str, organization: str, position: str, start_date: int, comments: str, is_verified: bool, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.joinCompany(email, organization, position, start_date, comments, is_verified))
    return hcRes(detail="Joined company successfully")

@router.post("/promoteEmployee", dependencies=[Depends(EmployeeCookie)])
async def promote_employee(email: str, organization: str, new_position: str, date: int, comments: str, is_verified: bool, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.promoteEmployee(email, organization, new_position, date, comments, is_verified))
    return hcRes(detail="Employee promoted successfully")

@router.post("/endEmployment", dependencies=[Depends(EmployeeCookie)])
async def end_employment(email: str, organization: str, date: int, status: int, comments: str, is_verified: bool, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.endEmployment(email, organization, date, status, comments, is_verified))
    return hcRes(detail="Employment ended successfully")

@router.get("/getCurrentEmployment", dependencies=[Depends(EmployeeCookie)])
async def get_current_employment(email: str):
    return hcRes(data=blockchain.functions.getCurrentEmployment(email).call())

@router.get("/getEmploymentHistory", dependencies=[Depends(EmployeeCookie)])
async def get_employment_history(email: str):
    return hcRes(data=blockchain.functions.getEmploymentHistory(email).call())

@router.post("/addDocument", dependencies=[Depends(EmployeeCookie)])
async def add_document(email: str, document_type: int, title: str, document_id: str, file_name: str, file_url: str, json_data: str, verified_by: str, date: int, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.addDocument(email, document_type, title, document_id, file_name, file_url, json_data, verified_by, date))
    return hcRes(detail="Document added successfully")

@router.get("/getDocument", dependencies=[Depends(EmployeeCookie)])
async def get_document(email: str, document_hash: str):
    return hcRes(data=blockchain.functions.getDocument(email, document_hash).call())

@router.get("/getDocumentHashes", dependencies=[Depends(EmployeeCookie)])
async def get_document_hashes(email: str):
    return hcRes(data=blockchain.functions.getDocumentHashes(email).call())

@router.get("/getAllDocuments", dependencies=[Depends(EmployeeCookie)])
async def get_all_documents(email: str):
    return hcRes(data=blockchain.functions.getAllDocuments(email).call())

@router.post("/addSkill", dependencies=[Depends(EmployeeCookie)])
async def add_skill(email: str, skill: str, score: int, verified_by: str, date: int, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.addSkill(email, skill, score, verified_by, date))
    return hcRes(detail="Skill added successfully")

@router.get("/getSkillScore", dependencies=[Depends(EmployeeCookie)])
async def get_skill_score(email: str, skill: str):
    return hcRes(data=blockchain.functions.getSkillScore(email, skill).call())

@router.get("/getSkills", dependencies=[Depends(EmployeeCookie)])
async def get_skills(email: str):
    return hcRes(data=blockchain.functions.getSkills(email).call())

@router.post("/addAccessKey", dependencies=[Depends(EmployeeCookie)])
async def add_access_key(email: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.addAccessKey(email))
    return hcRes(detail="Access key added successfully")

@router.post("/disableAccessKey", dependencies=[Depends(EmployeeCookie)])
async def disable_access_key(email: str, access_key: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.disableAccessKey(email, access_key))
    return hcRes(detail="Access key disabled successfully")























#######################


@router.post("/addDocument", dependencies=[Depends(EmployeeCookie)])
async def addDocument(
    documentType: Annotated[str, Form()],
    district: Annotated[str, Form()] = None,
    passing_year: Annotated[str, Form()] = None,
    panno: Annotated[str, Form()] = None,
    upload: Annotated[bytes, File()] = None,
    roll_number: Annotated[str, Form()] = None,
    session_data: SessionData = Depends(verifier),
    ):

    if documentType == "10th" or documentType == "12th":
        if district is None or passing_year is None or upload is None:
            raise hcCustomException(detail="Invalid data")
        
        if documentType == "10th":
            data = UPBOARD_HS_MARKSHEET_API(int(passing_year), district, roll_number)
        else:
            data = UPBOARD_SS_MARKSHEET_API(int(passing_year), district, roll_number)
        
        if "error" in data and data["error"] is not None:
            raise hcCustomException(detail=data["error"])
        
        return hcRes(detail="Document added successfully", data=data["data"])
    
    if documentType == "pan":
        if panno is None or upload is None:
            raise hcCustomException(detail="Invalid data")
        
        URL = "https://app-moneyview.whizdm.com/loans/services/api/lending/nsdl"
        req = requests.post(URL, data={"pan": panno}, verify=False, headers={"x-mv-app-version":"433"})
        if req.status_code == 200:
            return hcRes(detail="Status Fatched Success", data=req.json())
        
        raise hcCustomException(detail="Invalid PAN number")


    return hcRes(detail="Document added successfully", data="File uploaded successfully")