import requests as req
import re
from bs4 import BeautifulSoup
 
def get_schedule(username, password):
 
    url = "https://registrar.nu.edu.kz"
    r = req.Session()
    html = r.get(url + "/my-registrar").text
 
    csrfTokenReg = re.compile(r'name="csrf_token" value="(.+?)"')
    csrfMatch = csrfTokenReg.finditer(html)
    for match in csrfMatch:
        csrfToken = match.group(1)
    formIdReg = re.compile(r'name="form_build_id" value="(.+?)"')
    formMatch = formIdReg.finditer(html)
    for match in formMatch:
        formBuildId = match.group(1)
    headersPost = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5",
                   "Accept-Encoding": "gzip, deflate",
                   "Referer": "https://registrar.nu.edu.kz/user/login",
                   "Content-Type": "application/x-www-form-urlencoded",
                   
                   "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    data = {"csrf_token": csrfToken, "name": username, "pass": password,
            "form_build_id": formBuildId, "form_id": "user_login",
            "op": "Log in"}
 
    r.post(url + '/index.php?q=user/login', headers=headersPost, data=data)
    lol = r.post(url + '/index.php?q=user/login', headers=headersPost, data=data)
 
    headersGet = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://registrar.nu.edu.kz/index.php?q=user/login',
        'DNT': '1',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1'
 
    }
    text = r.get(r'https://registrar.nu.edu.kz/my-registrar/personal-schedule/json?method=drawStudentSchedule', headers=headersGet)
    raw_schedule = BeautifulSoup(text.text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
        
    #print(raw_schedule)

    grades_table = raw_schedule.find('div', class_='student_class_schedule_reports')
    
    if grades_table is None:
        return {}
    
    trs = grades_table.find_all('tr')

    schedule = {}
    curDay = None

    for j in range(1, len(trs)):
        tr = trs[j]
        tds = tr.find_all('td')    
        cur = []
        for i in range(0, len(tds) - 5):
            cur.append(tds[i].text.strip())
        if len(cur) == 0:
            curDay = tds[0].text.strip()
            continue
        subject = {
            'start_time': cur[0],
            'end_time': cur[1],
            'lecture_room': cur[2],
            'course_name': cur[3]
        }
        if not curDay in schedule:
            schedule[curDay] = []
        schedule[curDay].append(subject)

    return schedule

print(get_schedule('temirzhan.yussupov', '515563515563aA'))