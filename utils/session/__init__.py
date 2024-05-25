from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi import HTTPException
from uuid import UUID
from hcResponseBase import hcSuccessModal, hcCustomException, hcRes
from utils.session.memory import InDetaSHBackend, SessionData



cookie_params = CookieParameters()

# Uses UUID
AdminCookie = SessionCookie(cookie_name="administrator",identifier="general_verifier",auto_error=True,secret_key="DONOTUSE",cookie_params=cookie_params)
EmployeeCookie = SessionCookie(cookie_name="employee",identifier="general_verifier",auto_error=True,secret_key="DONOTUSE",cookie_params=cookie_params)
EmployerCookie = SessionCookie(cookie_name="employer",identifier="general_verifier",auto_error=True,secret_key="DONOTUSE",cookie_params=cookie_params)

backend = InDetaSHBackend[UUID, SessionData]()

class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True
    

verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=hcCustomException(status_code=401, detail="Not authenticated")
)