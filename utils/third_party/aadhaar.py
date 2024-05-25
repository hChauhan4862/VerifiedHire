import requests
import time
requests.packages.urllib3.disable_warnings() 

def demographic_auth(uid: str, name: str, gender: str):
    
    # create session for request
    s = requests.Session()
    s.headers.update({
        'Host': 'scholarships.punjab.gov.in',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://scholarships.punjab.gov.in',
        'Referer': 'https://scholarships.punjab.gov.in/public/AadharAuthenticationaspx.aspx',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    })

    # get request
    r = s.get("https://scholarships.punjab.gov.in/public/AadharAuthenticationaspx.aspx",verify=False, timeout=3)
    if r.status_code != 200:
        return {"error": "Failed to connect API"}
        
    
    viewstate = r.text.split('id="__VIEWSTATE" value="')[1].split('"')[0]
    viewstategenerator = r.text.split('id="__VIEWSTATEGENERATOR" value="')[1].split('"')[0]

    # post request
    r = s.post("https://scholarships.punjab.gov.in/public/AadharAuthenticationaspx.aspx",verify=False, data={
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        'ctl00$dpPH$txtAadhaarNumber': uid,
        'ctl00$dpPH$txtname': name,
        'ctl00$dpPH$ddlGender': gender,
        'ctl00$dpPH$txtVerifyCaptcha': 'TbjYsh',
        'ctl00$dpPH$btnCheckAuthentication': 'Authenticate',
        'ctl00$hdnisauthendicate': '0'
    }, timeout=3)

    if r.status_code != 200:
        return {"error": "Failed to connect API"}

    if "SucessShowPopup();" in r.text:
        return {"error": "success", "message": "Aadhaar Authentication Successful"}
    elif 'ShowPopup();' in r.text:
        error = r.text.split('<span id="ctl00_dpPH_lblmsg" style="color:Red;font-size:15px;">')[1].split('</span>')[0]
        return {"error": error }
    else:
        return {"error": "Could Not Verify Aadhaar Details"}

if __name__ == "__main__":
    r = demographic_auth("922302970901", "Harendra Chauhan", "M")
    print(r)