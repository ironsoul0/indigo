import requests 
from bs4 import BeautifulSoup

def get_grades(username, password):
  url = 'https://moodle.nu.edu.kz/login/index.php'
  r = requests.Session()
  payload = {
      'username': username,
      'password': password,
      'rememberusername': '0'
  }
  r.post(url, data=payload)
  html_doc = r.get('https://moodle.nu.edu.kz/grade/report/overview/index.php').text
  soup = BeautifulSoup(html_doc, 'html.parser')
  overview_grade = soup.find(id='overview-grade')
  if overview_grade is None:
    r.close()
    return {}
  grades_table = overview_grade.tbody
  trs_grades = grades_table.find_all('tr', class_="")

  courses = {}

  for tr_grade in trs_grades:
    course_link = tr_grade.td.a
    course_name = course_link.text
    course_href = course_link.get('href')
    html_doc = r.get(course_href).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    tr_itemnames = soup.find_all('tr')
    courses[course_name] = []
    
    for item_tr in tr_itemnames:
      column_itemname = item_tr.find('th', class_='column-itemname')
      column_grade = item_tr.find('td', class_='column-grade')
      column_range = item_tr.find('td', class_='column-range')
      column_percentage = item_tr.find('td', class_='column-percentage')

      if column_grade is None or column_itemname is None:
        continue

      if len(column_grade.text) < 2: # case when '-' or ''
        continue
      if 'mean of grades' in column_itemname.text.lower():
        continue
      if 'среднее взвешенное' in column_itemname.text.lower():
        continue 
      if 'course total' in column_itemname.text.lower():
        continue
      if 'attendance' in column_itemname.text.lower():
        continue
      
      grade_item = {}
      grade_item['name'] = column_itemname.text
      grade_item['grade'] = column_grade.text
      if not column_range is None and len(column_range.text) > 1:
        grade_item['range'] = column_range.text
      if not column_percentage is None and len(column_percentage.text) > 1:
        grade_item['percentage'] = column_percentage.text
      courses[course_name].append(grade_item)

  r.close()
  return courses
