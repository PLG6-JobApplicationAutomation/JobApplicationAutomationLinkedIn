from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time  # Needed for Bot to pause

ACCOUNT_EMAIL = input("Enter Email : ")  # Insert User email ""
ACCOUNT_PASSWORD = input("Enter Password : ")  # Insert User Password ""
PHONE = input("Enter Phone Number : ")  # Insert User Phone Number ""

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3318747866&geoId=107042567&keywords=cloud%20support"
    "%20engineer&location=Adelaide%2C%20South%20Australia%2C%20Australia&refresh=true")   # Insert Hyperlink For
# LinkedIn Search Job-Role/Location ""

time.sleep(2)
sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")  # Find Sign in Button
sign_in_button.click()

time.sleep(5)
email_field = driver.find_element(By.ID, "username")  # Find Email text box
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.ID, "password")  # Find Password text box
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

time.sleep(5)

all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in all_listings:
    print("called")
    listing.click()
    time.sleep(2)
    try:
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        apply_button.click()

        time.sleep(5)
        phone = driver.find_element(By.CLASS_NAME, "fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(PHONE)

        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()

            time.sleep(2)
            discard_button = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()

        time.sleep(2)
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()

    except NoSuchElementException:
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()

# Works for Easy Apply Ads on LinkedIn Only
# Will skip Other complex Ads on LinkedIn Automatically
