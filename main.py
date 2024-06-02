# Import necessary modules and classes
from fastapi import FastAPI, Depends, HTTPException, Request, status, Security, Path, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, StreamingResponse
from hcResponseBase import hcCustomException
from fastapi.exceptions import RequestValidationError, FastAPIError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
from io import BytesIO
from routes.api import router as api_router
from db import DetaObj as deta, blockchain, blockChainTransact
from dotenv import load_dotenv
import os
from fastapi import UploadFile

# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI(
    title="Verified Hire API", 
    version="V1",
    responses={200:{}},
)
# template_directory = "templates"
# templates = Jinja2Templates(directory=template_directory)

@app.exception_handler(hcCustomException)
async def unicorn_exception_handler(request: Request, exc: hcCustomException):
    if exc.detail == "" and exc.status_code in [403,422,429]:
        return HTMLResponse(status_code=exc.status_code, content="")

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "error_code": exc.error_code, "detail": exc.detail, "data" : exc.data},
        headers=exc.headers
    )

@app.exception_handler(Exception)
async def handle_exceptions(request, exc):
    error_msg = {"error": True, "error_code": 500 , "detail" : str(exc), "data" : {}}
    return JSONResponse(error_msg, status_code=status.HTTP_400_BAD_REQUEST)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # print(exc.errors())
    try:
        print(exc.errors())
        variable = exc.errors()[0]["loc"][1]
    except Exception as e:
        variable = ""
    error_msg = {"error": True, "error_code": 422 , "detail" : "Invalid value for "+ str(variable), "data" : {}}
    return JSONResponse(error_msg, status_code=status.HTTP_400_BAD_REQUEST)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000","*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base routes
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


app.include_router(api_router)




# Setup for templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/{path:path}", name="page", include_in_schema=False)
async def read_template(request: Request, path: str):
    if path == "" or path == "/":
        return templates.TemplateResponse("home.html", {"request": request})
    # Construct the template filename based on the path
    template_file = f"{path}.html"
    if os.path.exists("templates/" + template_file):
        return templates.TemplateResponse(template_file, {"request": request})
    
    # If the template file does not exist, raise a 404 error
    raise HTTPException(status_code=404, detail="File not found")



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True, server_header=False)