import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from settings import *

class HipoScraper:
    def __init__(self, site_url : str):
        self.site_url = site_url
    
    def scrape_jobs(self, job_title : str, skills : list, location : str):
        options = Options()
        options.binary_location = GOOGLE_CHROME_BIN
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.headless = True
        driver = webdriver.Chrome(options=options, executable_path=GOOGLE_CHROME_DRIVER_PATH)

        search_url = self.site_url

        # Location
        if location:
            search_url += '/' + location + '/'
        else:
            search_url += '/Toate-Orasele/'

        # Job Title
        if job_title:
            words = job_title.split(' ')
            for idx, w in enumerate(words):
                search_url += w
                if idx != len(words) - 1:
                    search_url += '-'
            if skills:
                search_url += '-'

        # Skills
        for idx, skill in enumerate(skills):
            search_url += str(skill)
            if idx != len(skills) - 1:
                search_url += '-'

        # Get last page
        jobs = []
        driver.get(search_url)
        ret_jobs = driver.find_elements(By.CLASS_NAME, "job-title")
        companies = driver.find_elements(By.CLASS_NAME, "cell-company")
        for i, job in enumerate(ret_jobs):
            company_name = companies[i].find_element(By.TAG_NAME, "span").text
            title = job.get_attribute('title')
            link = job.get_attribute('href')
            job = {}
            job["job_title"] = title
            job["company_name"] = company_name
            job["url"] = link
            jobs.append(job)
            if i == MAX_JOBS:
                break
        driver.quit()
        return jobs

    def scrape_candidates(self, job_title : str, skills : list, location : str):
        return {}
