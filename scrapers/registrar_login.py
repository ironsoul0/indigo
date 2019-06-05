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
  headersPost = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://registrar.nu.edu.kz/user/login",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
  }
  data = {
    "csrf_token": csrfToken, 
    "name": username, 
    "pass": password,
    "form_build_id": formBuildId, 
    "form_id": "user_login",
    "op": "Log in"
  }
  r.post(url + '/index.php?q=user/login', headers=headersPost, data=data)
  r.post(url + '/index.php?q=user/login', headers=headersPost, data=data)
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
  text = r.get(r'https://registrar.nu.edu.kz/my-registrar/personal-schedule/json?method=drawStudentSchedule&type=reg', headers=headersGet)
  raw_schedule = BeautifulSoup(text.text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
  grades_table = raw_schedule.find('div', class_='student_class_schedule_reports')
  if grades_table is None:
    return {}
  grades_rows = grades_table.find_all('tr')
  schedule = {}
  current_day = None
  for j in range(1, len(grades_rows)):
    grades_row = grades_rows[j]
    subject_parts = grades_row.find_all('td')    
    lecture_entity = []
    for i in range(0, len(subject_parts) - 5):
      lecture_entity.append(subject_parts[i].text.strip())
    if len(lecture_entity) == 0:
      current_day = subject_parts[0].text.strip()
      continue
    subject = {
      'start_time': lecture_entity[0],
      'end_time': lecture_entity[1],
      'lecture_room': lecture_entity[2],
      'course_name': lecture_entity[3]
    }
    if not current_day in schedule:
      schedule[current_day] = []
    schedule[current_day].append(subject)
  return schedule