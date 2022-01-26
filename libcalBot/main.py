import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


## Define the path to chromedriver
## Downloaded from https://chromedriver.storage.googleapis.com/index.html
## Version check by type 'chrome://version/' in browser search bar, eg. 97.0.4692.71
path = r"/Users/moyang"
os.environ['PATH'] += os.pathsep + path
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get("https://tilburguniversity.libcal.com/r")


reserve_btn = driver.find_element(By.ID, "s-lc-new-reservation-start")
reserve_btn.click()


name_input = driver.find_element(By.ID, "username")
name_input.send_keys("123")

password_input = driver.find_element(By.ID, "password")
password_input.send_keys("123")

login_btn = driver.find_element(By.CSS_SELECTOR,
            'button[name="login"]'
        )
login_btn.click()

## select location
select_loc = Select(driver.find_element(By.ID, "s-lc-location"))
select_loc.select_by_visible_text("CUBE building")

select_cap = Select(driver.find_element(By.ID, "s-lc-type"))
select_cap.select_by_value("1")

confirm_btn = driver.find_element(By.ID, "s-lc-go")
confirm_btn.click()

## hit next button
next_btn = driver.find_element(By.CSS_SELECTOR,
  'button[aria-label="Next"]'
)
prev_btn = driver.find_element(By.CSS_SELECTOR,
  'button[aria-label="Previous"]'
)

while True:
  next_btn.click()
  warning = driver.find_element(By.ID, "s-lc-window-limit-warning").get_attribute('style')
  if "none" not in warning:
    break


# while True:
#   prev_btn.click()
#   warning = driver.find_element(By.ID, "s-lc-window-limit-warning").get_attribute('style')
#   if "none" in warning:
#     break

prev_btn.click()

wait = WebDriverWait(driver, 10)
available = wait.until(EC.element_to_be_clickable((
  By.CSS_SELECTOR, "a[title*='8:30am'][title*='CUBE 29 - Available']"
  )))

### Select Time Slot
# available = driver.find_element(By.CSS_SELECTOR, "a[title*='8:30am'][title*='CUBE 29 - Available']")
available.click()

## Submit time
submit_time_btn = driver.find_element(By.ID, "submit_times")
submit_time_btn.click()

## Input student number
num_input = driver.find_element(By.ID, "q1045")
num_input.send_keys(921964)

corona_check = driver.find_element(By.CSS_SELECTOR, 'input[value="I have no Corona complaints"]')
corona_check.click()

### submit booking
booking_btn = driver.find_element(By.ID, "s-lc-eq-bform-submit")
booking_btn.click()
