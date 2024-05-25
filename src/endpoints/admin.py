from src.endpoints._base import *
from src.models.administrator import *
from uuid import uuid4

#APIRouter creates path operations for item module
router = APIRouter(
    prefix="/admin",
    tags=["Administrator"],
)

@router.post("/login")
async def login(response: Response, username: str = Body(example="admin@verifiedhire.in"), password: str = Body()):
    if not blockchain.functions.doesUserExist("admin@verifiedhire.in").call():
        a = blockChainTransact(blockchain.functions.registerUser(
            "Administrator", "admin@verifiedhire.in", Gender.Male , "9758684152", UserType.Admin, "Admin@123"
        ))
        a = blockChainTransact(blockchain.functions.activateUser(
            "admin@verifiedhire.in", "Auto Approve", "System"
        ))
    
    session = uuid4()
    a = blockChainTransact(blockchain.functions.login(username, password, str(session), UserType.Admin))
    AdminCookie.attach_to_response(response, session)
    return hcRes(detail="Login successful")

@router.post("/logout")
async def logout(response: Response, session_id: UUID = Depends(AdminCookie)):
    AdminCookie.delete_from_response(response)
    blockchain.functions.logout(str(session_id)).call()
    return hcRes(detail="Logout successful")

@router.get("/whoami", dependencies=[Depends(AdminCookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getAdminProfile(session_data.username).call())

@router.post("/changePassword", dependencies=[Depends(AdminCookie)])
async def change_password(new_password: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.changePassword(session_data.username, new_password))
    return hcRes(detail="Password changed successfully")

@router.get("/allusers", dependencies=[Depends(AdminCookie)])
async def all_users(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.listAllUsers().call())

@router.post("/updateProfilePic", dependencies=[Depends(AdminCookie)])
async def update_profile_pic(filename: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateProfilePic(session_data.username, filename))
    return hcRes(detail="Profile picture updated successfully")

@router.get("/getProfilePic", dependencies=[Depends(AdminCookie)])
async def get_profile_pic(session_data: SessionData = Depends(verifier)):
    return hcRes(data=blockchain.functions.getProfilePic(session_data.username).call())



###################### OTHER USER RELETED HANDLERS ######################
@router.get("/viewUserProfile", dependencies=[Depends(AdminCookie)])
async def view_user_profile(email: str, session_data: SessionData = Depends(verifier)):
    userType=blockchain.functions.getUserType(email).call()
    if userType == 0:
        return hcRes(data=blockchain.functions.getAdminProfile(email).call())
    elif userType == 1:
        return hcRes(data=blockchain.functions.getOrganizationProfile(email).call())
    elif userType == 2:
        return hcRes(data=blockchain.functions.getEmployeeProfile(email).call())

@router.get("/getCurrentStatus", dependencies=[Depends(AdminCookie)])
async def get_current_status(email: str):
    return hcRes(data=blockchain.functions.getCurrentStatus(email).call())

@router.post("/deactivateUser", dependencies=[Depends(AdminCookie)])
async def deactivate_user(email: str, reason: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.deactivateUser(email, reason, session_data.username))
    return hcRes(detail="User deactivated successfully")

@router.post("/activateUser", dependencies=[Depends(AdminCookie)])
async def activate_user(email: str, reason: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.activateUser(email, reason, session_data.username))
    return hcRes(detail="User activated successfully")

@router.get("/getStatusHistory", dependencies=[Depends(AdminCookie)])
async def get_status_history(email: str):
    return hcRes(data=blockchain.functions.getStatusHistory(email).call())

@router.get("/getCurrentAddress", dependencies=[Depends(AdminCookie)])
async def get_current_address(email: str):
    return hcRes(data=blockchain.functions.getCurrentAddress(email).call())

@router.get("/getUserCreditsHistory", dependencies=[Depends(AdminCookie)])
async def get_user_credits_history(email: str):
    return hcRes(data=blockchain.functions.getUserCreditsHistory(email).call())

@router.post("/updateCredits", dependencies=[Depends(AdminCookie)])
async def update_credits(email: str, credits: int, txn_comment: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.updateCredits(email, credits, txn_comment, session_data.username))
    return hcRes(detail="Credits updated successfully")

@router.get("/getDocument", dependencies=[Depends(AdminCookie)])
async def get_document(email: str, document_hash: str):
    return hcRes(data=blockchain.functions.getDocument(email, document_hash).call())

@router.get("/getDocumentHashes", dependencies=[Depends(AdminCookie)])
async def get_document_hashes(email: str):
    return hcRes(data=blockchain.functions.getDocumentHashes(email).call())

@router.get("/getAllDocuments", dependencies=[Depends(AdminCookie)])
async def get_all_documents(email: str):
    return hcRes(data=blockchain.functions.getAllDocuments(email).call())

@router.post("/verifyDocument", dependencies=[Depends(AdminCookie)])
async def verify_document(email: str, document_hash: str, session_data: SessionData = Depends(verifier)):
    a = blockChainTransact(blockchain.functions.verifyDocument(email, document_hash, session_data.username))
    return hcRes(detail="Document verified successfully")

@router.get("/getSkills", dependencies=[Depends(AdminCookie)])
async def get_skills(email: str):
    return hcRes(data=blockchain.functions.getSkills(email).call())

@router.get("/getSkillScore", dependencies=[Depends(AdminCookie)])
async def get_skill_score(email: str, skill: str):
    return hcRes(data=blockchain.functions.getSkillScore(email, skill).call())

# @router.post("/addAccessKey", dependencies=[Depends(AdminCookie)])
# async def add_access_key(email: str, session_data: SessionData = Depends(verifier)):
#     a = blockChainTransact(blockchain.functions.addAccessKey(email))
#     return hcRes(detail="Access key added successfully")

# @router.post("/disableAccessKey", dependencies=[Depends(AdminCookie)])
# async def disable_access_key(email: str, access_key: str, session_data: SessionData = Depends(verifier)):
#     a = blockChainTransact(blockchain.functions.disableAccessKey(email, access_key))
#     return hcRes(detail="Access key disabled successfully")