from fastapi import APIRouter, Request, Response, Depends, Form, UploadFile, File
from typing import Annotated

from starlette.responses import RedirectResponse
from typing import List, Optional, Annotated
from fastapi import Query, Path, Body
from fastapi.responses import FileResponse, StreamingResponse

from io import BytesIO

from hcResponseBase import hcSuccessModal, hcCustomError, hcRes
from db import deta_obj as deta, blockchain, blockChainTransact
from utils.session import *