from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from random import randint
import random
import sqlite3

user_agents = [
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
    'user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0']

class UpWorkBrowsing:

    def __init__(self):
        self.upwork_url = 'https://www.upwork.com/ab/account-security/login'

    def start_driver(self, user_agent: str):
        '''
        Load Selenium driver settings.
        :return: Selenium driver with the settings loaded.
        '''
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(user_agent)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        return driver

    def login(self, username: str, password: str, secret_answer: str, user_agent: str):
        '''
        Do the login process on Upwork page.
        :param username: User sername.
        :param password: User password.
        :param secret_answer: User account secret answer, it will be user if the site requests.
        :param user_agent: Browser user agent from list.
        :return: The selenium driver with the user home page loaded.
        '''
        driver = self.start_driver(user_agent)
        driver.get(self.upwork_url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_username"]')))
        time.sleep(randint(2,3))
        driver.find_element(By.XPATH,'//*[@id="login_username"]').send_keys(username)
        driver.find_element(By.XPATH,'//*[@id="login_password_continue"]').click() 
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_password"]')))
        time.sleep(randint(2,3))
        driver.find_element(By.XPATH,'//*[@id="login_password"]').send_keys(password)
        driver.find_element(By.XPATH,'//*[@id="login_control_continue"]').click() 
        time.sleep(randint(2,3))
        try:
            driver.find_element(By.XPATH,'//*[@id="login_answer"]')
            driver.find_element(By.XPATH,'//*[@id="login_answer"]').send_keys(secret_answer)
            driver.find_element(By.XPATH,'//*[@id="login_control_continue"]').click()
        except:
            print('No secret question!')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="job-tile-list"]')))
        time.sleep(randint(2,3))

        return driver

    def close_incomplete_profile_container(self, driver):
        '''
        Check if a screen asking to complete the profile is showed, if it appears, then close button is clicked and browsing is allowed.
        :param driver: Selenium driver on home page.
        :return: Selenium driver on same page and screen closed.
        '''
        try:
            driver.find_element(By.CSS_SELECTOR, 'div[class="profile-completeness-modal-container up-loader-container"]')
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        except:
            print('No Incomplete profile screen.')

        return driver

    def browse_to_most_recent(self, driver):
        '''
        Browse to most recent page.
        :param driver: Selenium driver on home page.
        :return: Selenium driver on most recent page.
        '''
        driver.find_element(By.CSS_SELECTOR,'button[data-test="tab-most-recent"]').click() 
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="job-tile-list"]')))
        time.sleep(randint(2,3))

        return driver

    def browse_to_jobs_saved(self, driver):
        '''
        Browse to jobs saved.
        :param driver: Selenium driver on most recent page.
        :return: Selenium driver on saved jobs.
        '''
        driver.find_element(By.CSS_SELECTOR,'button[data-test="tab-saved-jobs"]').click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="job-tile-list"]'))) 

        return driver

    def browse_to_settings(self, driver, secret_answer):
        '''
        Browse to profile settings.
        :param driver: Selenium driver on jobs saved page.
        :return: Selenium driver on profile settings page.
        '''
        driver.find_element(By.XPATH,'//*[@id="nav-right"]/ul/li[11]/button/div/img').click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-cy="menu-item-trigger"]')))
        driver.find_element(By.XPATH,'//*[@id="nav-right"]/ul/li[11]/ul/li[4]/ul/li[1]/a').click()
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="deviceAuth_answer"]')))
            driver.find_element(By.CSS_SELECTOR,'input[id="deviceAuth_answer"]').send_keys(secret_answer)
            driver.find_element(By.CSS_SELECTOR,'button[button-role="save"]').click()
        except:
            print('No secret answer req on settings.')

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="col-md-9"]')))
        time.sleep(randint(1,2))

        return driver

    def log_out(self, driver):
        '''
        Do the log out process.
        :param driver: Selenium driver on profile settings page.
        :return: Selenium driver on login page.
        '''
        driver.find_element(By.XPATH,'//*[@id="nav-right"]/ul/li[11]/button/div/img').click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-cy="menu-item-trigger"]')))
        driver.find_element(By.XPATH,'//*[@id="nav-right"]/ul/li[11]/ul/li[4]/ul/li[2]/button/span[2]').click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_username"]')))
        time.sleep(randint(2,3))

        return driver

class UpWorkScanner:

    def get_soup_object(self, driver):
        '''
        Get the Selenium driver with the current page data and translate it to a BeautifulSoup object.
        :param driver: Selenium driver with current page.
        :return: BeautifulSoup object.
        '''
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        return soup

    def get_user_details(self, soup: BeautifulSoup):
        '''
        Extract the profile name and title of the logged user.
        :param soup: BeautifulSoup object with the html data.
        :return: The profile name and the profile title.
        '''       
        profile = soup.find('h3', class_='mt-20 mb-0 text-decoration-underline')
        profile_title = soup.find('p', class_='mt-5 mb-0 ellipsis')

        return profile, profile_title

    def get_jobs(self, soup: BeautifulSoup):
        '''
        Scrape the jobs list.
        :param soup: BeautifulSoup object with jobs to scrape.
        :return: The jobs, details, descriptions and skills of all jobs available on the page.
        '''
        jobs = soup.find_all('h4', class_='my-0 p-sm-right job-tile-title')
        details = soup.find_all('small', class_='text-muted display-inline-block text-muted')
        descriptions = soup.find_all('div', class_='up-line-clamp-v2 clamped')[1:]
        skills = soup.find_all('div', class_='up-skill-wrapper')

        return jobs, details, descriptions, skills

    def profile_info(self, soup: BeautifulSoup):
        '''
        Scrape the profile info.
        :param soup: Beautiful Soup object with html from profile settings page.
        :return: The user id, address and phone.
        '''
        user_id = soup.find(attrs={'data-test' : 'userId'})
        address = soup.find(attrs={'data-test' : 'address'})
        phone = soup.find(attrs={'data-test' : 'phone'})

        return user_id, address, phone

class utils:

    def create_list_with_jobs_data(self, jobs: list, details: list, descriptions: list, skills: list):
        '''
        Create a list with the jobs data.
        :param jobs: Jobs titles.
        :param details: Details of the jobs.
        :param descriptions: Descriptions of the jobs.
        :param skills: Skills of the jobs.
        :return: A list of all jobs available.
        '''
        list_aux = []
        for job, detail, description, skill in zip(jobs, details, descriptions, skills):
            list_aux.append({'job': job.text.strip(), 'detail': detail.text.strip(), 'description': description.text.strip(), 'skill': skill.text.strip()})

        return list_aux

class files_operations:

    def save_dict_to_json(self, dictionary: dict):
        '''
        Save dictionary with profiles data to a JSON file.
        :param dictionary: Dictionary with profiles data.
        '''
        with open('profiles.json','r+') as file:
            file_data = json.load(file)
            file_data['profiles'].append(dictionary)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

if __name__ == '__main__':    
    browse = UpWorkBrowsing()
    scraper = UpWorkScanner()
    files_ops = files_operations()
    connection = sqlite3.connect('creds.db')
    cursor = connection.cursor()
    query = "select username, password, secret_answer FROM upwork_credentials"
    cursor.execute(query)
    users_list = cursor.fetchall()
    for user in users_list:
        browser_user_agent = random.choice(user_agents)
        driver = browse.login(user[0], user[1], user[2], browser_user_agent)
        soup = scraper.get_soup_object(driver)
        profile, profile_title = scraper.get_user_details(soup)
        jobs, details, descriptions, skills = scraper.get_jobs(soup)
        profile_data = {                
                        'name': profile.text.strip(), 
                        'title': profile_title.text.strip(), 
                        'user_id': None,
                        'address': None,
                        'phone': None,
                        'best_matches': {},
                        'most_recent' : {},
                        'saved_jobs' : {}
                        }
        list_aux = utils().create_list_with_jobs_data(jobs, details, descriptions, skills)
        profile_data['best_matches'] = list_aux

        driver = browse.close_incomplete_profile_container(driver)
        driver = browse.browse_to_most_recent(driver)
        soup = scraper.get_soup_object(driver)
        jobs, details, descriptions, skills = scraper.get_jobs(soup)
        list_aux = utils().create_list_with_jobs_data(jobs, details, descriptions, skills)
        profile_data['most_recent'] = list_aux

        driver = browse.browse_to_jobs_saved(driver)
        soup = scraper.get_soup_object(driver)
        jobs, details, descriptions, skills = scraper.get_jobs(soup)
        list_aux = utils().create_list_with_jobs_data(jobs, details, descriptions, skills)
        profile_data['saved_jobs'] = list_aux

        driver = browse.browse_to_settings(driver, user[2])
        soup = scraper.get_soup_object(driver)
        user_id, address, phone = scraper.profile_info(soup)
        profile_data['user_id'] = user_id.text.strip()
        profile_data['address'] = address.text.strip()
        profile_data['phone'] = phone.text.strip()

        files_ops.save_dict_to_json(profile_data)

        driver = browse.log_out(driver)
        driver.close()