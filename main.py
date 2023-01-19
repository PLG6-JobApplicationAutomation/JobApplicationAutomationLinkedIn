from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json


class EasyApplyLinkedin:

    def __init__(self, data):
        # Parameter initialization of Program includes User Email, Password, Keywords, Location and Service for
        # Chrome WebDriver from json file

        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def login_linkedin(self):
        # Function To automatically log in LinkedIn

        # Go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # Automatically input email and password and hit enter
        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)

    def job_search(self):
        # Function to go to the job page on LinkedIn anf filter Jobs by specified Keywords and Location

        # Go to Jobs
        jobs_link = self.driver.find_element(By.LINK_TEXT, 'Jobs')
        jobs_link.click()
        time.sleep(2)

        # Search based on keywords and location and hit enter
        search_keyword = self.driver.find_element(By.XPATH,
                                                  "//input[starts-with(@id,'jobs-search-box-keyword')]")
        search_keyword.clear()
        search_keyword.send_keys(self.keywords)
        time.sleep(2)
        search_location = self.driver.find_element(By.XPATH,
                                                   "//input[starts-with(@id,'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(2)
        search_location.send_keys(Keys.RETURN)

    def filter(self):
        # Filter all Jobs by the Easy Apply button

        # Select all filters, click on Easy Apply and apply the filter
        all_filters_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='All filters']")
        all_filters_button.click()
        time.sleep(1)
        iframe = self.driver.find_element(By.XPATH, "//div[@id='ember1428']")
        ActionChains(self.driver) \
            .scroll_to_element(iframe) \
            .perform()
        easy_apply_button = self.driver.find_element(By.XPATH, "//div[@id='ember1082']")
        easy_apply_button.click()
        time.sleep(1)
        apply_filter_button = self.driver.find_element(By.XPATH, "//button[@id='ember1096']")
        apply_filter_button.click()

    def find_offers(self):
        # Function finds all the offers through all the pages result of the search and filter

        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough
        # all available pages)
        total_results = self.driver.find_element(By.CLASS_NAME, "display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", ""))
        print(total_results_int)

        time.sleep(2)
        # Get results for the first page
        current_page = self.driver.current_url
        results = self.driver.find_elements(By.CLASS_NAME,
                                            "occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0"
                                            ".ember-view")

        # For each job add, submits application if no complex questions are asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = result.find_elements(By.CLASS_NAME,
                                          'job-card-search__title.artdeco-entity-lockup__title.ember-view')
            for title in titles:
                self.submit_apply(title)

        # If there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)

            # Find the last page and construct url of each page based on the total amount of pages
            find_pages = self.driver.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator.artdeco'
                                                                  '-pagination__indicator--number')
            total_pages = find_pages[len(find_pages) - 1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
            get_last_page = self.driver.find_element(By.XPATH,
                                                     "//button[@aria-label='Page " + str(total_pages_int) + "']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            total_jobs = int(last_page.split('start=', 1)[1])

            # Go through all available pages and job offers and apply
            for page_number in range(25, total_jobs + 25, 25):
                self.driver.get(current_page + '&start=' + str(page_number))
                time.sleep(2)
                results_ext = self.driver.find_elements(By.CLASS_NAME,
                                                        "occludable-update.artdeco-list__item--offset-4.artdeco"
                                                        "-list__item.p0.ember-view")
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements(By.CLASS_NAME,
                                                          'job-card-search__title.artdeco-entity-lockup__title.ember'
                                                          '-view')
                    for title_ext in titles_ext:
                        self.submit_apply(title_ext)
        else:
            self.close_session()

    def submit_apply(self, job_add):
        # Function submits the application

        print('You are applying to the position of: ', job_add.text)
        job_add.click()
        time.sleep(2)

        # Click on the easy apply button, skip if already applied for the add
        try:
            in_apply = self.driver.find_element(By.XPATH, "//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.click()
        except NoSuchElementException:
            print('You already applied to this job, go to next...')
            pass
        time.sleep(1)

        # Try to submit if submit application is available...
        try:
            submit = self.driver.find_element(By.XPATH, "//button[@data-control-name='submit_unify']")
            submit.send_keys(Keys.RETURN)

        # ... if not available, discard application and go to next
        except NoSuchElementException:
            print('Not direct application, going to next...')
            try:
                discard = self.driver.find_element(By.XPATH, "//button[@data-test-modal-close-btn]")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-test-dialog-primary-btn]")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass

        time.sleep(1)

    def close_session(self):
        # Function to close current session

        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        # Apply to Jobs

        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.filter()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_session()


if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()
