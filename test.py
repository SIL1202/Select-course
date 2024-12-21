import requests
from bs4 import BeautifulSoup

# URLs
base_url = "https://sys.ndhu.edu.tw/AA/CLASS/subjselect/"
login_url = base_url + "Default.aspx"
search_url = base_url + "course_pre_sele.aspx"

# 使用者帳號與密碼
username = "411221426"  # 你的學號
password = "2004.12.02"  # 你的密碼

# 建立 Session
session = requests.Session()

# 1. 登入系統
def login():
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 取得隱藏欄位
    viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
    event_validation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]

    # 登入資料
    payload = {
        "ctl00$ContentPlaceHolder1$ed_StudNo": username,
        "ctl00$ContentPlaceHolder1$ed_pass": password,
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": event_validation,
        "ctl00$ContentPlaceHolder1$BtnLoginNew": "登入"
    }
    session.post(login_url, data=payload)
    print("登入成功！")

# 2. 搜尋課程
def search_course(course_name):
    # 發送 GET 請求以取得搜尋頁面
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": search_url,
    }
    response = session.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 檢查 __VIEWSTATE 和 __EVENTVALIDATION
    viewstate = soup.find("input", {"name": "__VIEWSTATE"})
    event_validation = soup.find("input", {"name": "__EVENTVALIDATION"})

    if not viewstate or not event_validation:
        print("找不到 __VIEWSTATE 或 __EVENTVALIDATION，請檢查 session 狀態！")
        print(response.text)  # 輸出內容進一步排查
        return None

    viewstate = viewstate["value"]
    event_validation = event_validation["value"]

    # 送出搜尋課程的 POST 請求
    payload = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": event_validation,
        "ctl00$ContentPlaceHolder1$tbxKeyword": course_name,  # 課程名稱關鍵字
        "ctl00$ContentPlaceHolder1$btnQuery": "查詢"
    }
    response = session.post(search_url, data=payload, headers=headers)
    print(f"搜尋課程: {course_name} 完成！")
    return response.text

# 3. 提交選課請求
def select_course(course_values):
    for course_name, course_value in course_values.items():
        payload = {
            "__VIEWSTATE": "",
            "__EVENTVALIDATION": "",
            "ctl00$ContentPlaceHolder1$add": course_value  # 選課按鈕的 value
        }
        response = session.post(search_url, data=payload)
        if "成功" in response.text:  # 根據回傳內容確認結果
            print(f"課程 {course_name} 預排成功！")
        else:
            print(f"課程 {course_name} 預排失敗！")

# 執行流程
login()
course_names = ["藝術概論", "音樂與藝術"]  # 要搜尋的課程名稱
selected_courses = search_course(course_names)
select_course(selected_courses)

