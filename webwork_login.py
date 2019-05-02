import requests
import json
import re
from bs4 import BeautifulSoup

def get_course_webworks(URL, login, passwd):    
  course_webworks = [] 
  response = requests.post(
    URL, 
    files={
      'user': (None, login), 
      'passwd': (None, passwd)
    }
  )
  success_pattern = re.compile(r'Logged in as {}'.format(login))    
  if success_pattern.search(response.text):
    soup_entry = BeautifulSoup(response.text, 'html.parser')
    webwork_rows = soup_entry.table.find_all('tr')
    for single_row in webwork_rows:
      webwork_entities = single_row.find_all('td')
      if len(webwork_entities) > 1:
        if 'closed' in webwork_entities[-1].text.lower():
          continue
        course_webworks.append('{} - {}'.format(webwork_entities[1].text, webwork_entities[-1].text)) 
    return course_webworks
  else:
    raise("Couldn't login")

def get_webworks(login, passwd):
  webworks_URL = "http://webwork.sst.nu.edu.kz/"
  page_text = requests.get(webworks_URL).text
  login_link_pattern = re.compile(r'<a href="/(.+?)/">(.+?)</a>')
  available_courses = []
  for course_match in login_link_pattern.finditer(page_text):
    available_courses.append(course_match.group(1))  
  webworks = {}
  for course in available_courses: 
    try:
      course_webworks = get_course_webworks(webworks_URL + course, login, passwd)
      webworks[course] = course_webworks
    except:
      pass
  return webworks