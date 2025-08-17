import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

COOKIES_FILE = "lk.json"
PROFILE_URL = "https://www.linkedin.com/in/navyasrik/"


def scroll_until_about(driver, max_scrolls=10):
    for _ in range(max_scrolls):
        try:
            elem = driver.find_element(
                By.XPATH, "//div[contains(@class,'display-flex') and contains(@class,'pv3')]"
            )
            return elem.text.strip()
        except NoSuchElementException:
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
    return None

def load_cookies(driver, cookies_file):
    with open(cookies_file, "r") as f:
        cookies = json.load(f)
    driver.get("https://www.linkedin.com")
    for cookie in cookies:
        # Selenium requires domain without leading dot
        if "sameSite" in cookie:
            cookie.pop("sameSite")  # Prevent invalid arg error
        driver.add_cookie(cookie)
    driver.refresh()

def scrape_profile(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Can be removed if you want to see browser
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load cookies to bypass login
        load_cookies(driver, COOKIES_FILE)

        driver.get(url)

        # Get name
        try:
            name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            ).text.strip()
        except:
            name = None

        # Get headline
        try:
            headline = driver.find_element(By.CLASS_NAME, "text-body-medium").text.strip()
        except:
            headline = None

        # Get bio
        try:
            
            bio = scroll_until_about(driver)
            
        except:
            bio = None

        return {"name": name, "headline": headline, "bio": bio}

    finally:
        driver.quit()

if __name__ == "__main__":
    data = scrape_profile(PROFILE_URL)
    print(json.dumps(data, indent=2))
