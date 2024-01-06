import logging
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
# Set up Chrome options for running in headless mode

import time


def element_locator(elem):
    try:
        found_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(elem)
        )
        return found_elem
    except NoSuchElementException:
        logging.info(f"{elem} was not found")


page_elements = {
        "login": (By.XPATH, "//input[@id='userNameInput']"),
        "next_button": (By.XPATH, "//span[@id='nextButton']"),
        "password": (By.XPATH, "//input[@id='passwordInput']"),
        "submit": (By.XPATH, "//span[@id='submitButton']"),
        "status":(By.XPATH, "/html[1]/body[1]/usos-layout[1]/div[2]/main-panel[1]/main[1]/div[1]/div[1]/usos-frame[1]/div[2]/table[1]/tbody[1]/tr[6]/td[2]/span[1]")
    }


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)


url = 'https://usosweb.ue.wroc.pl/kontroler.php?_action=logowaniecas/index'
driver.get(url)

# CREDENTIALS
user_id = <<ENTER USER ID HERE>>
user_password = <<ENTER USER PASSWORD HERE>>

# login
login_page = element_locator(page_elements["login"])
ActionChains(driver).send_keys_to_element(login_page, user_id).perform()
# next
element_locator(page_elements["next_button"]).click()
# password
password = element_locator(page_elements["password"])
ActionChains(driver).send_keys_to_element(password, user_password).perform()
# next
element_locator(page_elements["submit"]).click()


diploma_page = "https://usosweb.ue.wroc.pl/kontroler.php?_action=dla_stud/studia/dyplomy/index"
driver.get(diploma_page)

status = element_locator(page_elements["status"]).text

print(status)

input("Press Enter to continue...")

# Close the browser window
driver.quit()

