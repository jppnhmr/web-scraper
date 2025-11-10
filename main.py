import requests
import time
from bs4 import BeautifulSoup as bs

URL = "https://www.python.org/jobs/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} # If 403 Forbidden comes up

KWS = ["python", "node.js", "restful", "graphql", "mysql", "postgresql", "monogodb", "redis", "aws", "linux", "ai", "machine learning", "http", "ssl", "docker", "kubernetes", "ci", "cd", "api design", "system design", "distributed systems",]
WAIT = 0.5 # for set time between requests

class Job:
    def __init__(self, url, title):
        self.url = url
        self.title = title

        self.soup = get_soup(self.url)

        self.description = self.extract_description()
        self.keywords_found = self.extract_keywords()
        self.job_types = self.extract_job_types()

    def extract_description(self):
        node = self.soup.select_one(".job-description")
        return node.get_text(separator=" ", strip=True) if node else " "

    def extract_keywords(self):
        text = self.description.lower()
        found = []

        for kw in KWS:
            if kw in text:
                found.append(kw)

        return found
    
    def extract_job_types(self):
        job_types = []

        a_tags = self.soup.select(".listing-job-type a")
        if a_tags != None:
            job_types = [a.get_text(strip=True) for a in a_tags]
        else:
            print("Failed to find 'a tags'")

        return job_types
    
    def get_job_types(self):
        return self.job_types
        
    def get_keywords(self):
        return self.keywords_found

                
def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        exit()

    return bs(response.text, 'html.parser')

def get_jobs(soup):
    target_class = 'listing-company-name'
    jobs = soup.find_all(class_=target_class)
    print(f"Found {len(jobs)} job listings.")

    job_objs = []
    for job in jobs:
        full_link = None
        job_title = None

        link_element = job.find('a')
        if link_element != None:
            href = link_element.get('href')
            job_title = link_element.text.strip()
            if href != None:
                full_link = f"{URL}{href[6:]}" # don't include '/jobs/' from href
        
        job_objs.append(Job(full_link, job_title))

    return job_objs

if __name__ == "__main__":

    soup = get_soup(URL)
    print("--- Extracting Job Info ---")
    jobs = get_jobs(soup)
    print("--- Job Info Extracted ---")

    # Populate Keyword and Job Type dictionaries
    kw_count_dict = {}
    jb_types_count_dict = {}
    for job in jobs:

        kws_found = job.get_keywords()
        for kw in kws_found:
            kw_count_dict[kw] = kw_count_dict.get(kw, 0) + 1

        jb_types_found = job.get_job_types()
        for jb_t in jb_types_found:
            jb_types_count_dict[jb_t] = jb_types_count_dict.get(jb_t, 0) + 1

        time.sleep(WAIT)

    # Plot histograms
    # TODO

    # Save to CSV
    with open("python_jobs.csv", "w+") as csv:

        # Title # URL # Job Type # Keywords # 
        csv.write("Title, URL, Job Type, Keywords\n")

        for job in jobs:
            csv.write(f"{job.title},{job.url},{job.get_job_types()},{job.get_keywords()}\n")

    print("--- Finished ---")