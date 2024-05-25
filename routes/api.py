from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import APIRouter, status
from hcResponseBase import hcCustomError, hcSuccessModal, hcRes
from hcErrors import hcCustomException, ValidationError
from src.endpoints import admin,employees,recruiters
from src.models._base import *
import random   
import requests
import smtplib
import os


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

class SendOTP(BaseModel):
    phone: str = Form(..., title="Phone No", max_length=10, pattern="^[0-9]{10}$")
    email: EmailStr = Form(..., title="Email ID")

@router.post("/sendotp")
async def send_otp( r : SendOTP):
    otp_sms = str(random.randint(1000, 9999))
    otp_mail = str(random.randint(100000, 999999))
    url = "https://www.fast2sms.com/dev/voice?authorization="+os.getenv("FAST2SMS_TOKEN")+"&route=otp&variables_values="+otp_sms+"&numbers="+r.phone
    url2 = "https://www.fast2sms.com/dev/bulkV2?authorization="+os.getenv("FAST2SMS_TOKEN")+"&route=otp&flash=0&variables_values="+otp_sms+"&numbers="+r.phone
    response = requests.request("GET", url)
    print(response.text)
    if response.status_code != 200:
        raise hcCustomException(detail="OTP sending failed")
    
    # response = requests.request("GET", url2)
    # print(response.text)
    # if response.status_code != 200:
    #     raise hcCustomException(detail="OTP sending failed")
    
    s = smtplib.SMTP(os.getenv("SMTP_ADDRESS"),os.getenv("SMTP_PORT"))
    s.starttls()
    s.login(os.getenv("SMTP_ACCOUNT"),os.getenv("SMTP_PASSWORD"))
    sender_email_id = os.getenv("SMTP_SENDER")

    # Message content
    body = f"Hi Mr./Mrs.,\n\nWelcome to the Verified-Hire portal!.\n\nWe are providing a blockchain empowered background verification for the professionals. Here is your user OTP for your registeration: \nOTP : {otp_mail}\n\n\nRegards,\nVerified-Hire Team."
    msg = MIMEMultipart()
    msg['From'] = sender_email_id
    msg['To'] = r.email
    msg['Subject'] = "Verified Hire OTP"
    # Attach the message body
    msg.attach(MIMEText(body, 'plain'))
    # sending the mail
    s.sendmail(sender_email_id, r.email, msg.as_string())
    
    noisy_otp_sms = ""
    for digit in otp_sms:
        noisy_otp_sms += digit
        noisy_otp_sms += chr(random.randint(65, 90))
    
    noisy_otp_mail = ""
    for digit in otp_mail:
        noisy_otp_mail += digit
        noisy_otp_mail += chr(random.randint(65, 90))

    return hcRes(detail="OTP sent successfully", data={
        "sms": noisy_otp_sms,
        "mail": noisy_otp_mail
    })

router.include_router(admin.router)
router.include_router(employees.router)
router.include_router(recruiters.router)