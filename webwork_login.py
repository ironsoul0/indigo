import requests
import json
import re
from bs4 import BeautifulSoup

def login_to_course(url, login, passwd):    
  result = [] 
  response = requests.post(url, files={'user': (None, login), 'passwd': (None, passwd)})
  successPat = re.compile(r'Logged in as {}'.format(login))    
  if successPat.search(response.text):
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.table.find_all('tr')
    for tr in trs:
      tds = tr.find_all('td')
      if len(tds) > 1:
        if 'closed' in tds[-1].text.lower():
          continue
        result.append('{} - {}'.format(tds[1].text, tds[-1].text)) 
    return result
  else:
    raise("Couldn't login")

def get_webworks(login, passwd):
    print(login, passwd)
    url = "http://webwork.sst.nu.edu.kz/"
    pageText = requests.get(url).text
    loginLinkPat = re.compile(r'<a href="/(.+?)/">(.+?)</a>')
    link_list = []
    cnt = 0
    for match in loginLinkPat.finditer(pageText):
        link_list.append(match.group(1))    
    
    courses = {}

    for course in link_list: 
        try:
            sets = login_to_course(url + course, login, passwd)
            courses[course] = sets
            cnt += 1
        except:
            pass
    if cnt == 0:
      return {'fail': [ ]}
    return courses
  
print(get_webworks('temirzhan.yussupov', '201747150'))