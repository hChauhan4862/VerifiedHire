from src.endpoints._base import *
from src.models._base import *
from uuid import uuid4
import random   
import requests
import smtplib
import os

#APIRouter creates path operations for item module
router = APIRouter(
    prefix="",
    tags=["Common"]
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
        "sms": otp_sms,
        "mail": otp_mail
    })


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to Deta.sh
        fname = str(uuid4()) + file.filename
        file_content = await file.read()
        deta.files.all_files.put(fname, file_content)
        return hcRes(detail="File uploaded successfully",data={"key": fname})
    except Exception as e:
        print(e)
        raise hcCustomException(detail="Failed to upload file", status_code=500)

@router.get("/files/{key}")
async def ViewFile(key: str):
    try:
        file = deta.files.all_files.get(key)
        return StreamingResponse(BytesIO(file.read()))
    except Exception as e:
        raise hcCustomException(detail="File not found", status_code = 404)