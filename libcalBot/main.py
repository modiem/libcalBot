import libcalBot.constants as const
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Booking(webdriver.Chrome):

  ## Define the path to chromedriver
  ## Downloaded from https://chromedriver.storage.googleapis.com/index.html
  ## Version check by type 'chrome://version/' in browser search bar, eg. 97.0.4692.71
  def __init__(self, driver_path = r"/Users/moyang"):
    self.driver_path = driver_path
    os.environ['PATH'] += os.pathsep + driver_path
    options = webdriver.ChromeOptions()
    super(Booking, self).__init__(options=options)
    self.implicitly_wait(5)
    self.maximize_window()

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.quit()

  def to_reserve_page(self):
    self.get(const.BASE_URL)
    reserve_btn = self.find_element(By.ID, "s-lc-new-reservation-start")
    reserve_btn.click()

  def login(self):
    name_input = self.find_element(By.ID, "username")
    name_input.send_keys(os.environ['UNUMBER'])
    password_input = self.find_element(By.ID, "password")
    password_input.send_keys(os.environ['PASS_WORD'])
    login_btn = self.find_element(By.CSS_SELECTOR,
            'button[name="login"]'
        )
    login_btn.click()

  def select_loc(self):
    ## select location
    select_loc = Select(self.find_element(By.ID, "s-lc-location"))
    select_loc.select_by_visible_text("CUBE building")

    ## select study room
    select_cap = Select(self.find_element(By.ID, "s-lc-type"))
    select_cap.select_by_value("1")

    ## confirm choices
    confirm_btn = self.find_element(By.ID, "s-lc-go")
    confirm_btn.click()

  def to_date(self):
    ## hit next button
    next_btn = self.find_element(By.CSS_SELECTOR,
      'button[aria-label="Next"]'
    )
    prev_btn = self.find_element(By.CSS_SELECTOR,
      'button[aria-label="Previous"]'
    )

    ## Hit the next btn until the warning showing
    ## that the current day is unavailable
    while True:
      next_btn.click()
      warning_display = self.find_element(By.ID, "s-lc-window-limit-warning").get_attribute('style')
      if "none" not in warning_display:
        break

    ## go to the previous day
    ## this would be the new day available for booking
    prev_btn.click()

  def pick_room(self, capacity = "1"):
    self.room = const.ROOMS[capacity][0]


  def reserve_room(self, time="8:30am"):
    self.time = time
    wait = WebDriverWait(self, 10)
    available = wait.until(EC.element_to_be_clickable((
      By.CSS_SELECTOR, f"a[title*='{self.time}'][title*='CUBE {self.room} - Available']"
    )))
    available.click()

    ## Submit time
    submit_time_btn = self.find_element(By.ID, "submit_times")
    submit_time_btn.click()

    ## Input student number
    num_input = self.find_element(By.ID, "q1045")
    num_input.send_keys(921964)

    corona_check = self.find_element(By.CSS_SELECTOR, 'input[value="I have no Corona complaints"]')
    corona_check.click()

    ### submit booking
    booking_btn = self.find_element(By.ID, "s-lc-eq-bform-submit")
    booking_btn.click()

  def make_another_reservation(self):
    btn = self.find_element(By.CSS_SELECTOR,
      'a[href="/r/new?lid=1937&gid=0&zone=0&capacity=1&accessible=0&powered=0"]'
    )
    btn.click()
