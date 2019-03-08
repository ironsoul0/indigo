import requests
import json
import re
from bs4 import BeautifulSoup
import requests 

def brute(r, cur = []):
  if len(cur) == 5:
    print(cur)
    payload = {
      'user': 'almat.sergazyyev',
      'effectiveUser': 'almat.sergazyyev',
      'templateName': 'system',
      'AnSwEr0001': cur[0],
      'AnSwEr0002': cur[1],
      'AnSwEr0003': cur[2],
      'AnSwEr0004': cur[3],
      'AnSwEr0005': cur[4],
      'submitAnswers': 'Submit Answers',
      'showOldAnswers': '1',
      'displayMode': 'MathJax'
    }
    r.post('http://webwork.sst.nu.edu.kz/webwork2/MATH-162-1L-Calc-II-Spring19/HW7/3/', data=payload)
  else:
    ans = ['NA', 'CONV', 'DIV']
    for x in ans:
      new_cur = cur.copy()
      new_cur.append(x)
      brute(r, new_cur)
      
def solve(user, passwd):
  url = 'http://webwork.sst.nu.edu.kz/webwork2/MATH-162-1L-Calc-II-Spring19/'
  r = requests.Session()
  payload = {
      'user': user,
      'passwd': passwd
  }
  content = r.post(url, data=payload)
  url = 'http://webwork.sst.nu.edu.kz/webwork2/MATH-162-1L-Calc-II-Spring19/HW7/3/'
  cur = []
  brute(r)

solve('almat.sergazyyev', '201711726')