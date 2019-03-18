import requests
import json
import re
from bs4 import BeautifulSoup
import requests 

userName = 'madi.raissov'
fixedLen = 5
variants = ['CONV', 'DIV', 'NA']
questionUrl = 'http://webwork.sst.nu.edu.kz/webwork2/MATH-162-1L-Calc-II-Spring19/HW7/3/'

def brute(r, cur = []):
  if len(cur) == fixedLen:
    payload = {
      'user': userName,
      'effectiveUser': userName,
      'templateName': 'system',
      'submitAnswers': 'Submit Answers',
      'showOldAnswers': '1',
      'displayMode': 'MathJax'
    }
    for i in range(fixedLen):
      answer_str = 'AnSwEr000{}'.format(i + 1)
      payload[answer_str] = cur[i]
    #print(payload)
    res = r.post(questionUrl, data=payload)
    if not 'NO' in res.text:
      print(cur)
  else:
    for x in variants:
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
  r.post(url, data=payload)
  brute(r)

solve(userName, '201717112')