import requests
from bs4 import BeautifulSoup
import json
import api_calls

START_URL = 'https://my.nu.edu.kz/wps/portal/hidden/login/!ut/p/b1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOKd3R09TMx9DAwsfNxNDTwdPUKDLAONjQ1czYEKIoEKDHAARwNC-sP1o_AqCTSBKsBjhZ9Hfm6qfkFuhEGWiaMiAFWLnI8!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_2OQEAB1A0GNQE0Q8VHS8J11082/act/id=0/407863574114/-/?login=temirzhan.yussupov&password=515563515563aA&loginSubmit=Login'

PARAMS = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Encoding':'gzip, deflate, br',
          'Accept-Language':'en-US,en;q=0.5',
          'Connection':'keep-alive',
          'Host':'my.nu.edu.kz',
          'Referer':'https://my.nu.edu.kz/wps/portal/hidden/login/!ut/p/b1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOKd3R09TMx9DAwsfNxNDTwdPUKDLAONjQ1czYEKIoEKDHAARwNC-sP1o_AqCTSBKsBjhZ9Hfm6qfkFuhEGWiaMiAFWLnI8!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/',
          'Upgrade-Insecure-Requests':'1',
          'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
          }

dict_pairs = {
    'School: ': 'school',
    'Major: ': 'major',
    'Year of study: ': 'studyYear',
    'Sex: ': 'sex',
    'Mobile Phone number: ': 'phone',
    'Date of birth: ': 'birthDate'
}

required_fields = ['id', 'name', 'surname', 'email', 'school', 'major', 'studyYear', 'sex', 'phone', 'birthDate']

def retrieve(string, substring):
    return string[len(substring):].strip()

def getInfo(student_id, s, auth_cookies):
    r = s.get('http://my.nu.edu.kz/.AccountPage/StudentCard?uid={}'.format(student_id), cookies=auth_cookies)

    result = r.text

    if len(result) > 80000:
    
        soup = BeautifulSoup(result, 'html.parser')

        student = {}

        divs = soup.find_all("div", class_="infoClass")

        fullName = divs[0].ul.find_all("li")[0].h3.text.strip()
        nameComponents = fullName.split()


        student['name'] = nameComponents[0]
        student['surname'] = nameComponents[1]
        student['email'] = nameComponents[0].lower() + '.' + nameComponents[1].lower() + '@nu.edu.kz'
        student['id'] = student_id
        
        for li in soup.find_all('li'):
            curText = li.text
            for requiredText, changedText in dict_pairs.items():
                if requiredText in curText:
                    student[changedText] = retrieve(curText, requiredText)
        
        for field in required_fields:
            if not field in student:
                student[field] = ''
        return student
        print(str(student) + ',')
        
    return {}

def get_name(username, s, auth_cookies):
  if username.count('.') != 1:
    return ''
  data = username.split('.')
  if len(data) != 2:
    return ''
  name = data[0]
  surname = data[1]

  payload = {
    'username': '{} {}'.format(name, surname),
    'organisationNumber': 'KS_ZUP_NU1',
    'organisationName': 'Назарбаев Университет',
    'departments': '',
    'linkSelected': '',
    'schoolVal': 'Year of Study',
    'school': 'select school',
    'courses': 'Year of Study',
    'usertype': 'Students',
    'maxRows': '25'
  }

  curHeaders = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'my.nu.edu.kz',
    'Origin': 'https://my.nu.edu.kz',
    'Referer': 'https://my.nu.edu.kz/.PhoneBookPortlet/PhoneBookPortletRedirectServlet',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
  }
  r = s.post('https://my.nu.edu.kz/.PhoneBookPortlet/UsernameServlet', headers=curHeaders, data=payload)
  res = json.loads(r.text)
  if len(res) != 1:
    return ''
  now = res[0]['rows']
  if len(now) != 1:
    return ''
  now = now[0]
  username = now['userName']
  splitted = username.split(' ')
  name = splitted[2]
  student_id = now['userid']
  student_info = getInfo(student_id, s, auth_cookies)
  sex = student_info['sex']
  if sex == 'Female':
    return name
  else:
    return ''
  
def get_girls():
  girls = []
  with requests.Session() as s:
    p = s.get(url = START_URL, params = PARAMS)
    chats = api_calls.get_all_chats_info()
    for chat in chats:
      if not 'username' in chat:
        continue
      username = chat['username']
      chat_id = chat['chat_id']
      result = get_name(username, s, p.cookies)
      if len(result) > 0:
        girls.append((result, chat_id))
        print('{} - {}'.format(girls[-1][0], girls[-1][1]))
  return girls