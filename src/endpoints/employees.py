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
async def login(response: Response, login_data: LoginModel = Body(...)):
    session = uuid4()
    a = blockChainTransact(blockchain.functions.login(login_data.username, login_data.password, str(session), UserType.Employee))
    EmployeeCookie.attach_to_response(response, session)
    return hcRes(detail="Login successful")
    

@router.post("/logout")
async def logout(response: Response, session_id: UUID = Depends(EmployeeCookie)):
    EmployeeCookie.delete_from_response(response)
    blockchain.functions.logout(str(session_id)).call()
    return hcRes(detail="Logout successful")

@router.get("/whoami", dependencies=[Depends(EmployeeCookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getEmployeeProfile(session_data.username).call())

@router.post("/updateUserDetails", dependencies=[Depends(EmployeeCookie)])
async def update_user_details(user_details: UpdateUserDetailsModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateUserDetails(session_data.username, user_details.name, user_details.gender, user_details.phone, user_details.user_type))
    return hcRes(detail="User details updated successfully")




@router.post("/changePassword", dependencies=[Depends(EmployeeCookie)])
async def change_password(password_data: ChangePasswordModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.changePassword(session_data.username, password_data.new_password))
    return hcRes(detail="Password changed successfully")

@router.get("/getStatusHistory", dependencies=[Depends(EmployeeCookie)])
async def get_status_history(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getStatusHistory(session_data.username).call())

@router.post("/updateAddress", dependencies=[Depends(EmployeeCookie)])
async def update_address(address_data: UpdateAddressModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateAddress(session_data.username, address_data.new_address))
    return hcRes(detail="Address updated successfully")

@router.get("/getCurrentAddress", dependencies=[Depends(EmployeeCookie)])
async def get_current_address(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getCurrentAddress(session_data.username).call())

@router.post("/updateProfilePic", dependencies=[Depends(EmployeeCookie)])
async def update_profile_pic(profile_pic_data: UpdateProfilePicModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateProfilePic(session_data.username, profile_pic_data.filename))
    return hcRes(detail="Profile picture updated successfully")

@router.get("/getProfilePic", dependencies=[Depends(EmployeeCookie)])
async def get_profile_pic(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getProfilePic(session_data.username).call())

@router.post("/joinCompany", dependencies=[Depends(EmployeeCookie)])
async def join_company(company_data: JoinCompanyModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.joinCompany(session_data.username, company_data.organization, company_data.position, company_data.start_date, company_data.comments, company_data.is_verified))
    return hcRes(detail="Joined company successfully")

@router.post("/promoteEmployee", dependencies=[Depends(EmployeeCookie)])
async def promote_employee(promote_data: PromoteEmployeeModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.promoteEmployee(session_data.username, promote_data.organization, promote_data.new_position, promote_data.date, promote_data.comments, promote_data.is_verified))
    return hcRes(detail="Employee promoted successfully")

@router.post("/endEmployment", dependencies=[Depends(EmployeeCookie)])
async def end_employment(employment_data: EndEmploymentModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.endEmployment(session_data.username, employment_data.organization, employment_data.date, employment_data.status, employment_data.comments, employment_data.is_verified))
    return hcRes(detail="Employment ended successfully")

@router.get("/getCurrentEmployment", dependencies=[Depends(EmployeeCookie)])
async def get_current_employment(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getCurrentEmployment(session_data.username).call())

@router.get("/getEmploymentHistory", dependencies=[Depends(EmployeeCookie)])
async def get_employment_history(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getEmploymentHistory(session_data.username).call())

@router.post("/addDocument", dependencies=[Depends(EmployeeCookie)])
async def add_document(document_data: AddDocumentModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.addDocument(session_data.username, document_data.document_type, document_data.title, document_data.document_id, document_data.file_name, document_data.file_url, document_data.json_data, document_data.verified_by, document_data.date))
    return hcRes(detail="Document added successfully")

@router.get("/getDocument", dependencies=[Depends(EmployeeCookie)])
async def get_document(document_hash: str = Body(...), session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getDocument(session_data.username, document_hash).call())

@router.get("/getDocumentHashes", dependencies=[Depends(EmployeeCookie)])
async def get_document_hashes(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getDocumentHashes(session_data.username).call())

@router.get("/getAllDocuments", dependencies=[Depends(EmployeeCookie)])
async def get_all_documents(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getAllDocuments(session_data.username).call())

@router.post("/addSkill", dependencies=[Depends(EmployeeCookie)])
async def add_skill(skill_data: AddSkillModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.addSkill(session_data.username, skill_data.skill, skill_data.score, skill_data.verified_by, skill_data.date))
    return hcRes(detail="Skill added successfully")

@router.get("/getSkillScore", dependencies=[Depends(EmployeeCookie)])
async def get_skill_score(skill: str = Body(...), session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getSkillScore(session_data.username, skill).call())

@router.get("/getSkills", dependencies=[Depends(EmployeeCookie)])
async def get_skills(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getSkills(session_data.username).call())


@router.post("/addAccessKey", dependencies=[Depends(EmployeeCookie)])
async def add_access_key(session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.addAccessKey(session_data.username))
    return hcRes(detail="Access key added successfully")

@router.post("/disableAccessKey", dependencies=[Depends(EmployeeCookie)])
async def disable_access_key(access_key_data: DisableAccessKeyModel = Body(...), session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.disableAccessKey(session_data.username, access_key_data.access_key))
    return hcRes(detail="Access key disabled successfully")


@router.post("/fetchDocumentUsingAPI", dependencies=[Depends(EmployeeCookie)])
async def fetch_document(document_data: FetchDocumentModel = Body(...), session_data: SessionData = Depends(verifier)):
    if document_data.document_type == "10th" or document_data.document_type == "12th":
        if document_data.district is None or document_data.passing_year is None:
            raise hcCustomException(detail="Invalid data")

        if document_data.document_type == "10th":
            data = UPBOARD_HS_MARKSHEET_API(int(document_data.passing_year), document_data.district, document_data.roll_number)
        else:
            data = UPBOARD_SS_MARKSHEET_API(int(document_data.passing_year), document_data.district, document_data.roll_number)

        if "error" in data and data["error"] is not None:
            raise hcCustomException(detail=data["error"])

        return hcRes(detail="Document added successfully", data=data["data"])

    if document_data.document_type == "pan":
        if document_data.panno is None:
            raise hcCustomException(detail="Invalid data")

        URL = "https://app-moneyview.whizdm.com/loans/services/api/lending/nsdl"
        req = requests.post(URL, data={"pan": document_data.panno}, verify=False, headers={"x-mv-app-version": "433"})
        if req.status_code == 200:
            return hcRes(detail="Status Fetched Success", data={
                "DOCUMENT_TYPE": "PAN_CARD",
                "pan": document_data.panno,
                "name": req.json()
            })

        raise hcCustomException(detail="Pan Number Details Could Not Found")

    raise hcCustomException(detail="Invalid data")