import requests
import json as JSON

def UPBOARD_HS_MARKSHEET_API(year: int, district: str, roll: str):
    MetaData = {
        2023 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_2023.aspx", "roll_length": 10, "district_required": True},
        2022 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_2022.aspx", "roll_length": 10, "district_required": True},
        2021 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_2021.aspx", "roll_length": 9, "district_required": True},
        2020 : {"url": "http://results.upmsp.edu.in/ResultHighSchool20152020.aspx", "roll_length": 7, "district_required": False},
        2019 : {"url": "http://results.upmsp.edu.in/ResultHighSchool20152020.aspx", "roll_length": 7, "district_required": False},
        2018 : {"url": "http://results.upmsp.edu.in/ResultHighSchool20152020.aspx", "roll_length": 7, "district_required": False},
        2017 : {"url": "http://results.upmsp.edu.in/ResultHighSchool20152020.aspx", "roll_length": 7, "district_required": False},
        2016 : {"url": "http://results.upmsp.edu.in/ResultHighSchool20152020.aspx", "roll_length": 7, "district_required": False},
        2015 : {"url": "http://results.upmsp.edu.in/ResultHighSchool20152020.aspx", "roll_length": 7, "district_required": False},
        2014 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20122015.aspx", "roll_length": 7, "district_required": True},
        2013 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20122015.aspx", "roll_length": 7, "district_required": True},
        2012 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20122015.aspx", "roll_length": 7, "district_required": True},
        2011 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC2011.aspx", "roll_length": 7, "district_required": False},
        2010 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC2010.aspx", "roll_length": 7, "district_required": True},
        2009 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20072009.aspx", "roll_length": 7, "district_required": False},
        2008 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20072009.aspx", "roll_length": 7, "district_required": False},
        2007 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20072009.aspx", "roll_length": 7, "district_required": False},
        2006 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20032006.aspx", "roll_length": 7, "district_required": False},
        2005 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20032006.aspx", "roll_length": 7, "district_required": False},
        2004 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20032006.aspx", "roll_length": 7, "district_required": False},
        2003 : {"url": "http://results.upmsp.edu.in/ResultHighSchool_NIC20032006.aspx", "roll_length": 7, "district_required": False}
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
    r = s.get("http://results.upmsp.edu.in/CaptchaImage.aspx?query=0.603525920530112&Code=AAAAAA", verify=False)
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
        "Origin": "http://results.upmsp.edu.in"
    }
    # print("Sending request:","\n", JSON.dumps(data, indent=4), "\n", JSON.dumps(headers, indent=4))
    r = s.request(method="POST", url=url, data=data, headers=headers, verify=False)
    if r.status_code != 200:
        return {"error": "Failed to connect API"}
    t = r.text
    
    # Parse the data
    RESULT = {}
    RESULT["DOCUMENT_TYPE"] = "HS_MARKSHEET"
    RESULT["CLASS"] = "High School"
    RESULT["BOARD_UNIVERSITY"] = "Uttar Pradesh Madhyamik Shiksha Parishad"
    RESULT["RESULT_TYPE"] = "YEAR_WISE"

    RESULT["ROLL"] = t.split('ctl00_cphBody_lbl_ROLL_NO">')[1].split('<')[0] if 'ctl00_cphBody_lbl_ROLL_NO">' in t else None
    RESULT["NAME"] = t.split('ctl00_cphBody_lbl_C_NAME">')[1].split('<')[0] if 'ctl00_cphBody_lbl_C_NAME">' in t else None
    RESULT["MOTHER"] = t.split('ctl00_cphBody_lbl_M_NAME">')[1].split('<')[0] if 'ctl00_cphBody_lbl_M_NAME">' in t else None
    RESULT["FATHER"] = t.split('ctl00_cphBody_lbl_F_NAME">')[1].split('<')[0] if 'ctl00_cphBody_lbl_F_NAME">' in t else None
    RESULT["DOB"] = t.split('ctl00_cphBody_lbl_DDMMYYYY">')[1].split('<')[0] if 'ctl00_cphBody_lbl_DDMMYYYY">' in t else None
    RESULT["STREAM"] = None
    RESULT["DIST_CODE"] = t.split('ctl00_cphBody_lbl_DISTT_CD">')[1].split('<')[0] if 'ctl00_cphBody_lbl_DISTT_CD">' in t else None
    RESULT["SCHOOL_CODE"] = t.split('ctl00_cphBody_lbl_SCHOOL_CD">')[1].split('<')[0] if 'ctl00_cphBody_lbl_SCHOOL_CD">' in t else None

    RESULT["MARKS"] = [] # List of dictionaries for each year or semester wise marks
    
    # Get the marks for first year
    marks = {
        "TABLE": {
            "HEADER": ["SUBJECT", "THEORY 1", "THEORY 2", "THEORY 3", "PRACTICAL", "GRACE", "TOTAL", "GRADE"],
            "DATA": []
        },
        "STATUS": "",
        "GRACE": None,
        "TOTAL": None,
        "OBTAINTED": None,
        "DIVISION": "",
    }

    Grand_Obtained = 0
    for i in range(1,7):
        SUBJECT = t.split(f'ctl00_cphBody_lbl_Sub{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_Sub{i}">' in t else None
        THEORY1 = t.split(f'ctl00_cphBody_lbl_PAP1_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP1_MK{i}">' in t else (t.split(f'ctl00_cphBody_lbl_MRK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_MRK{i}">' in t else None)
        THEORY2 = t.split(f'ctl00_cphBody_lbl_PAP2_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP2_MK{i}">' in t else None
        THEORY3 = t.split(f'ctl00_cphBody_lbl_PAP3_MK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_PAP3_MK{i}">' in t else None
        PRACTICAL = t.split(f'ctl00_cphBody_lbl_MRK_PRC{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_MRK_PRC{i}">' in t else (t.split(f'ctl00_cphBody_lbl_Prc{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_Prc{i}">' in t else None)
        GRACE = t.split(f'ctl00_cphBody_lbl_GRC{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_GRC{i}">' in t else None
        TOTAL = t.split(f'ctl00_cphBody_lbl_TOT_MRK{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_TOT_MRK{i}">' in t else (t.split(f'ctl00_cphBody_lbl_Tot{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_Tot{i}">' in t else None)
        GRADE = t.split(f'ctl00_cphBody_lbl_Grd{i}">')[1].split('<')[0] if f'ctl00_cphBody_lbl_Grd{i}">' in t else None

        if TOTAL is None:
            TOTAL = sum((int(THEORY1) if THEORY1 is not None else 0), (int(THEORY2) if THEORY2 is not None else 0), (int(THEORY3) if THEORY3 is not None else 0), (int(PRACTICAL) if PRACTICAL is not None else 0), (int(GRACE) if GRACE is not None else 0))
        Grand_Obtained += int(TOTAL)
        marks["TABLE"]["DATA"].append([SUBJECT, THEORY1, THEORY2, THEORY3, PRACTICAL, GRACE, TOTAL, GRADE])
    
    marks["GRACE"] = t.split('id="ctl00_cphBody_lbl_GRACE" style="font-size:0.9em">')[1].split('<')[0] if 'id="ctl00_cphBody_lbl_GRACE" style="font-size:0.9em">' in t else None
    marks["TOTAL"] = t.split(f'ctl00_cphBody_lbl_TOT_MRK">')[1].split('<')[0] if f'ctl00_cphBody_lbl_TOT_MRK">' in t else 600
    marks["OBTAINTED"] = t.split(f'ctl00_cphBody_lbl_OBTD_MRK">')[1].split('<')[0] if f'ctl00_cphBody_lbl_OBTD_MRK">' in t else Grand_Obtained
    marks["STATUS"] = t.split('ctl00_cphBody_lbl_RESULT">')[1].split('<')[0] if 'ctl00_cphBody_lbl_RESULT">' in t else None
    marks["DIVISION"] = t.split('ctl00_cphBody_lbl_DIVISION">')[1].split('<')[0] if 'ctl00_cphBody_lbl_DIVISION">' in t else None

    # Get the subjects
    RESULT["MARKS"].append(marks)

    return {"error": None, "data": RESULT}
    

if __name__ == "__main__":
    r = UPBOARD_HS_MARKSHEET_API(2016, "NA", "0377121")
    print(JSON.dumps(r, indent=4))
