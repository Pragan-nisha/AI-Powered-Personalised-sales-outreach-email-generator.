import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

COOKIES_FILE = R"C:\Users\Pragan Nisha\OneDrive\Desktop\wb\New folder\TOOLS\lk.json"  # Ensure this file is in the same folder as the script

def scroll_until_about(driver, max_scrolls=10):
    """Scroll until the About section is visible, or stop after max_scrolls."""
    for _ in range(max_scrolls):
        try:
            elem = driver.find_element(
                By.XPATH, "//div[contains(@class,'display-flex') and contains(@class,'pv3')]"
            )
            return elem.text.strip()
        except NoSuchElementException:
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.8)
    return None

def load_cookies(driver, cookies_file):
    """Load LinkedIn cookies from a JSON file to bypass login."""
    with open(cookies_file, "r") as f:
        cookies = json.load(f)
    driver.get("https://www.linkedin.com")
    for cookie in cookies:
        if "sameSite" in cookie:
            cookie.pop("sameSite")  # Avoid Selenium arg errors
        driver.add_cookie(cookie)
    driver.refresh()

def scrape_profile(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Comment out if debugging
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load cookies to stay logged in
        load_cookies(driver, COOKIES_FILE)
        driver.get(url)

        # Name
        try:
            name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            ).text.strip()
        except:
            name = None

        # Headline
        try:
            headline = driver.find_element(By.CLASS_NAME, "text-body-medium").text.strip()
        except:
            headline = None

        # Bio/About section
        try:
            bio = scroll_until_about(driver)
        except:
            bio = None

        return {"name": name, "headline": headline, "bio": bio}

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No profile URL provided"}))
        sys.exit(1)

    profile_url = sys.argv[1]
    data = scrape_profile(profile_url)
    print(json.dumps(data))
