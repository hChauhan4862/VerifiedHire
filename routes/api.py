from fastapi import APIRouter, status
from hcResponseBase import hcCustomError, hcSuccessModal, hcRes
from hcErrors import hcCustomException, ValidationError
from src.endpoints import admin,employees,recruiters, common



router = APIRouter(prefix="/api", 
        responses={
            status.HTTP_200_OK : {"model": hcSuccessModal},
        #     status.HTTP_400_BAD_REQUEST: {"model": hcCustomError},
        #     status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized Access | Token expired or Not valid"},
        #     status.HTTP_403_FORBIDDEN: {"description": "Forbidden Access | Scope Not Found"},
            status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationError},
        #     status.HTTP_429_TOO_MANY_REQUESTS: {},
        }
    )


router.include_router(common.router)
router.include_router(admin.router)
router.include_router(employees.router)
router.include_router(recruiters.router)