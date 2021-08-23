import requests
from bs4 import BeautifulSoup
# from extract_functions import get_last_page

URL = f"https://stackoverflow.com/jobs?q=python"
pagination_class = "s-pagination"

# print(get_last_page(URL, pagination_class))


def get_last_page():
    request = requests.get(URL)
    soup = BeautifulSoup(request.text, 'html.parser')
    pages = soup.find("div", {"class": pagination_class}).find_all("a")
    last_page = pages[-2].find("span").string
    # last_page = pages[-2].get_text(strip=True) #같음
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")['title']
    company_html, location_html = html.find("h3", {
        "class": "mb4"
    }).find_all("span", recursive=False)
    try:
        company = company_html.string.strip()
    except:
        company_html.span.replace_with('////')
        company = company_html.get_text(strip=True).split('////')[0]

    location = location_html.get_text(strip=True)
    job_id = html['data-jobid']
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
