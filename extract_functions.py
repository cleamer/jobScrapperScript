import requests
from bs4 import BeautifulSoup

def get_last_page(url, class_name):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div",{"class":f"{class_name}"})
  links=pagination.find_all('a')

  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  last_page = pages[-1]
  return last_page

