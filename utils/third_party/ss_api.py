import requests
import json as JSON

def UPBOARD_SS_MARKSHEET_API(year: int, district: str, roll: str):
    MetaData = {
        2023 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_2023.aspx", "roll_length": 10, "district_required": True},
        2022 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_2022.aspx", "roll_length": 10, "district_required": True},
        2021 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_2021.aspx", "roll_length": 9, "district_required": True},
        2020 : {"url": "https://results.upmsp.edu.in/ResultIntermediate20152020.aspx", "roll_length": 7, "district_required": False},
        2019 : {"url": "https://results.upmsp.edu.in/ResultIntermediate20152020.aspx", "roll_length": 7, "district_required": False},
        2018 : {"url": "https://results.upmsp.edu.in/ResultIntermediate20152020.aspx", "roll_length": 7, "district_required": False},
        2017 : {"url": "https://results.upmsp.edu.in/ResultIntermediate20152020.aspx", "roll_length": 7, "district_required": False},
        2016 : {"url": "https://results.upmsp.edu.in/ResultIntermediate20152020.aspx", "roll_length": 7, "district_required": False},
        2015 : {"url": "https://results.upmsp.edu.in/ResultIntermediate20152020.aspx", "roll_length": 7, "district_required": False},
        2014 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20072014.aspx", "roll_length": 7, "district_required": False},
        2013 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20072014.aspx", "roll_length": 7, "district_required": False},
        2012 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC2012.aspx", "roll_length": 7, "district_required": True},
        2011 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20072014.aspx", "roll_length": 7, "district_required": False},
        2010 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20072014.aspx", "roll_length": 7, "district_required": True},
        2009 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20072014.aspx", "roll_length": 7, "district_required": False},
        2008 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20072014.aspx", "roll_length": 7, "district_required": False},
        2007 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20072014.aspx", "roll_length": 7, "district_required": False},
        2006 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20032006.aspx", "roll_length": 7, "district_required": False},
        2005 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20032006.aspx", "roll_length": 7, "district_required": False},
        2004 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20032006.aspx", "roll_length": 7, "district_required": False},
        2003 : {"url": "https://results.upmsp.edu.in/ResultIntermediate_NIC20032006.aspx", "roll_length": 7, "district_required": False}
    }

    # Validate the input
    if year not in MetaData:
        return {"error": "Invalid year"}
    
    roll_length = MetaData[year]["roll_length"]
    district_required = MetaData[year]["district_required"]
    url = MetaData[year]["url"]
    
    if district_required and (not district.isdigit() or len(district) != 2):
        return {"error": "Invalid district"}
    if not roll.isdigit() or len(roll) != roll_length:
        return {"error": "Invalid roll number"}

    # Create a session
    s = requests.Session()

    # Get the initial page to get the viewstate and eventvalidation
    r = s.get(url)
    if r.status_code != 200:
        return {"error": "Failed to connect API"}
    res = r.text
    
    # Get the captcha
    r = s.get("https://results.upmsp.edu.in/CaptchaImage.aspx?query=0.603525920530112&Code=AAAAAA")
    if r.status_code != 200:
        return {"error": "Failed to connect API"}
    
    # Read the viewstate and eventvalidation
    viewstate = res.split('id="__VIEWSTATE" value="')[1].split('"')[0]
    eventvalidation = res.split('id="__EVENTVALIDATION" value="')[1].split('"')[0]
    VIEWSTATEGENERATOR = res.split('id="__VIEWSTATEGENERATOR" value="')[1].split('"')[0]

    # Prepare the data and headers for the POST request
    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
        "__VIEWSTATEENCRYPTED": "",
        "__EVENTVALIDATION": eventvalidation,
        "ctl00$cphBody$ddl_districtCode": district,
        "ctl00$cphBody$ddl_ExamYear": year,
        "ctl00$cphBody$txt_RollNumber": roll,
        "ctl00$cphBody$TxtCAPTCHA": "AAAAAA",
        "ctl00$cphBody$HiddenField_CaptchaCode": "AAAAAA",
        "ctl00$cphBody$btnSubmit": "View Result"
    }
    headers={
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "results.upmsp.edu.in",
        "Origin": "https://results.upmsp.edu.in"
    }
    # print("Sending request:","\n", JSON.dumps(data, indent=4), "\n", JSON.dumps(headers, indent=4))
    r = s.request(method="POST", url=url, data=data, headers=headers)
    if r.status_code != 200:
        return {"error": "Failed to connect API"}
    t = r.text
    
    # Parse the data
    RESULT = {}
    RESULT["DOCUMENT_TYPE"] = "SS_MARKSHEET"
    RESULT["CLASS"] = "High School"
    RESULT["BOARD_UNIVERSITY"] = "Uttar Pradesh Madhyamik Shiksha Parishad"
    RESULT["RESULT_TYPE"] = "YEAR_WISE"

    RESULT["ROLL"] = t.split('ctl00_cphBody_lbl_ROLL_NO">')[1].split('<')[0] if 'ctl00_cphBody_lbl_ROLL_NO">' in t else None
    RESULT["NAME"] = t.split('ctl00_cphBody_lbl_C_NAME">')[1].split('<')[0] if 'ctl00_cphBody_lbl_C_NAME">' in t else None
    RESULT["MOTHER"] = t.split('ctl00_cphBody_lbl_M_NAME">')[1].split('<')[0] if 'ctl00_cphBody_lbl_M_NAME">' in t else None
    RESULT["FATHER"] = t.split('ctl00_cphBody_lbl_F_NAME">')[1].split('<')[0] if 'ctl00_cphBody_lbl_F_NAME">' in t else None
    RESULT["DOB"] = None
    RESULT["STREAM"] = t.split('ctl00_cphBody_lbl_GROUP">')[1].split('<')[0] if 'ctl00_cphBody_lbl_GROUP">' in t else None
    RESULT["DIST_CODE"] = t.split('ctl00_cphBody_lbl_DISTT_CD">')[1].split('<')[0] if 'ctl00_cphBody_lbl_DISTT_CD">' in t else None
    RESULT["SCHOOL_CODE"] = t.split('ctl00_cphBody_lbl_SCHOOL_CD">')[1].split('<')[0] if 'ctl00_cphBody_lbl_SCHOOL_CD">' in t else None

    RESULT["MARKS"] = [] # List of dictionaries for each year or semester wise marks
    
    # Get the marks for first year
    marks = {
        "TABLE": {
            "HEADER": ["SUBJECT", "P1", "P2", "P3", "P4", "P5", "PRACTICAL", "TOTAL"],
            "DATA": []
        },
        "STATUS": "",
        "GRACE": None,
        "TOTAL": None,
        "OBTAINTED": None,
        "DIVISION": "",
    }

    for i in range(1,7):
        subject = t.split(f'ctl00_cphBody_lbl_SUBJ_{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_SUBJ_{i}">' in t else None
        p1 = t.split(f'ctl00_cphBody_lbl_PAP1_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP1_MK{i}">' in t else None
        p2 = t.split(f'ctl00_cphBody_lbl_PAP2_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP2_MK{i}">' in t else None
        p3 = t.split(f'ctl00_cphBody_lbl_PAP3_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP3_MK{i}">' in t else None
        p4 = t.split(f'ctl00_cphBody_lbl_PAP4_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP4_MK{i}">' in t else None
        p5 = t.split(f'ctl00_cphBody_lbl_PAP5_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP5_MK{i}">' in t else None
        practical = t.split(f'ctl00_cphBody_lbl_PRAC_MRK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PRAC_MRK{i}">' in t else None
        total = t.split(f'ctl00_cphBody_lbl_TOT_MRK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_TOT_MRK{i}">' in t else None
        marks["TABLE"]["DATA"].append([subject, p1, p2, p3, p4, p5, practical, total])
    
    marks["STATUS"] = t.split('ctl00_cphBody_lbl_RESULT">')[1].split('<')[0] if 'ctl00_cphBody_lbl_RESULT">' in t else None
    marks["TOTAL"] = t.split(f'ctl00_cphBody_lbl_TOT_MRK">')[1].split('<')[0] if f'ctl00_cphBody_lbl_TOT_MRK">' in t else None
    marks["OBTAINTED"] = t.split(f'ctl00_cphBody_lbl_OBTD_MRK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_OBTD_MRK{i}">' in t else None
    marks["DIVISION"] = t.split('ctl00_cphBody_lbl_DIVISION">')[1].split('<')[0] if 'ctl00_cphBody_lbl_DIVISION">' in t else None

    # Get the subjects
    RESULT["MARKS"].append(marks)

    return {"error": None, "data": RESULT}
    
if __name__ == "__main__":
    r = UPBOARD_SS_MARKSHEET_API(2018, "06", "0259117")
    print(JSON.dumps(r, indent=4))
