import requests
from bs4 import BeautifulSoup as bs

URL = "https://www.python.org/jobs/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} # If 403 Forbidden comes up

def get_soup(url):
    try:
        response = requests.get(url, HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        exit()

    return bs(response.text, 'html.parser')

def get_jobs_dict(soup):
    target_class = 'listing-company-name'
    jobs = soup.find_all(class_=target_class)
    print(f"Found {len(jobs)} job listings.")
    print("-"*60)

    jobs_dict = {}
    for job in jobs:
        full_link = None
        job_title = None

        link_element = job.find('a')
        if link_element != None:
            href = link_element.get('href')
            job_title = link_element.text.strip()
            if href != None:
                full_link = f"{URL}{href[6:]}" # don't include '/jobs/' from href

        jobs_dict[job_title] = full_link

    return jobs_dict

if __name__ == "__main__":

    soup = get_soup(URL)
    jobs_dict = get_jobs_dict(soup)

    for job in jobs_dict.items():
        print(job)
