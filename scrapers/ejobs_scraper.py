from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from settings import *

class EJobsScraper:
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

        if location:
            search_url += location + '/'
        
        if job_title:
            words = job_title.split(' ')
            for idx, word in enumerate(words):
                search_url += word
                if idx != len(words) - 1:
                    search_url += '-'
            if skills:
                search_url += '-'
        
        if skills:
            for idx, skill in enumerate(skills):
                search_url += str(skill)
                if idx != len(skills) - 1:
                    search_url += '-'

        jobs = []
        driver.get(search_url)
        job_cards = driver.find_elements(By.CLASS_NAME, 'JobCard')
        for idx, job_card in enumerate(job_cards):
            if idx == MAX_JOBS:
                break
            crt_company = job_card.find_element(By.CLASS_NAME, "JCContentMiddle").find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').text
            crt_job_title = job_card.find_element(By.CLASS_NAME, 'JCContentMiddle__Title').find_element(By.TAG_NAME, 'span').text
            crt_job_link = job_card.find_element(By.CLASS_NAME, 'JCContentMiddle__Title').find_element(By.TAG_NAME, 'a').get_attribute('href')
            job = {}
            job["job_title"] = crt_job_title
            job["company_name"] = crt_company
            job["url"] = crt_job_link
            jobs.append(job)
        driver.quit()

        return jobs
    
    def scrape_candidates(self, job_title : str, skills : list, location : str):
        return {}
