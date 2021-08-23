import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div",{"class":"pagination"})
  links=pagination.find_all('a')

  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  last_page = pages[-1]
  return last_page

def extract_job(html):
  title = html.find('h2', {"class" : "jobTitle"}).find('span', title = True)['title']
  company = html.find('span', {"class" : "companyName"})
  location = html.find('div', {"class" : "companyLocation"})
  job_id = html.parent['data-jk']
  if company:
    company = company.string
    if location:
      location = location.string
    else:
      location = None
  else:
    company = None
    if location:
      location = location.string
    else:
      location = None
  return {
      'title': title, 
      'company' : company , 
      'location' : location, 
      'link': f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}&from=web&vjs=3"
      } 
    
def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping indeed: Page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all('div', {"class":"slider_container"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs