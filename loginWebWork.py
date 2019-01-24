import requests
import re
from bs4 import BeautifulSoup

def tryToLogin(url, login, passwd):   
    result = []
    page_text = requests.get(url).text    
    response = requests.post(url, files={'user': (None, login), 'passwd': (None, passwd)})
    successPat = re.compile(r'Logged in as {}'.format(login))    
    if successPat.search(response.text):
        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            print(tds)
            print(len(tds) > 1)
            print()
            if len(tds) > 1:

                result.append(tds[1].text)
        return result
    else:
        raise("Couldn't login")

def loginToAll(login, passwd):
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
            sets = tryToLogin(url + course, login, passwd)
            courses[course] = sets
            cnt += 1
        except:
            pass
    return courses

print(loginToAll('temirzhan.yussupov', '201747150'))