from src.endpoints._base import *
from src.models.recruiter import *
from uuid import uuid4
import requests
import random

#APIRouter creates path operations for item module
router = APIRouter(
    prefix="/recruiter",
    tags=["Recruiter"]
)

@router.post("/signup")
async def register(r: Register):
    if blockchain.functions.doesUserExist(r.email).call():
        raise hcCustomException(detail="User already exists")
    

    a = blockChainTransact(blockchain.functions.registerUser(
        r.organization,
        r.email,
        2,  # Other
        r.phone,
        UserType.Organization,  # Assuming 1 is the user type for employer
        r.password
    ))

    return hcRes(detail="Registration successful")

@router.post("/login")
async def login(response: Response, username: str = Body(), password: str = Body()):
    session = uuid4()
    a = blockChainTransact(blockchain.functions.login(username, password, str(session), UserType.Organization))
    EmployerCookie.attach_to_response(response, session)
    return hcRes(detail="Login successful")

@router.post("/logout")
async def logout(response: Response, session_id: UUID = Depends(EmployerCookie)):
    EmployerCookie.delete_from_response(response)
    blockchain.functions.logout(str(session_id)).call()
    return hcRes(detail="Logout successful")

@router.get("/whoami", dependencies=[Depends(EmployerCookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getOrganizationProfile(session_data.username).call())

@router.get("/getEmployeeProfile", dependencies=[Depends(EmployerCookie)])
async def whoami(email: str, access_code: str, session_data: SessionData = Depends(verifier)):

    blockChainTransact(blockchain.functions.AccessKeyIsActive(email, access_code, session_data.username))

    blockChainTransact(blockchain.functions.updateCredits(session_data.username, -50, "View Profile For User "+ email, "System"))

    return hcRes(data=blockchain.functions.getEmployeeProfile(session_data.username).call())

@router.post("/verifyDocument", dependencies=[Depends(EmployerCookie)])
async def verify_document(email: str, document_hash: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.verifyDocument(email, document_hash, session_data.username))
    blockChainTransact(blockchain.functions.updateCredits(session_data.username, 20, "Verify document For User "+ email, "System"))
    return hcRes(detail="Document verified successfully")

@router.post("/addSkill", dependencies=[Depends(EmployerCookie)])
async def verify_document(email: str, skill: str, score: int, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.addSkill(email, skill, score, session_data.username))
    blockChainTransact(blockchain.functions.updateCredits(session_data.username, 20, "Verify document For User "+ email, "System"))
    return hcRes(detail="Document verified successfully")