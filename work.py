from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
# LOGIN AUTOMATION FUNCTION
def login_to_freelancer(username, password, login_url):
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(login_url)

    try:
        # Enter the username
        driver.find_element(By.ID, 'emailOrUsernameInput').send_keys(username)

        # Enter the password
        driver.find_element(By.ID, 'passwordInput').send_keys(password)

        # Wait until the login button is clickable
        wait = WebDriverWait(driver, 10)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'ButtonElement')]")))

        # Click the login button
        login_button.click()

        print("Login successful")
    except Exception as e:
        print("Login failed:", e)
        # Quit the driver if login fails
        driver.quit()

    return driver

def scrape_projects(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    # Taking the useful classes for scrapping the details.
    project_search_content = driver.find_element(By.CLASS_NAME, "ProjectSearch-content")
    project_cards = project_search_content.find_elements(By.CLASS_NAME, "JobSearchCard-item")
    # store all the details in data list so that we can make csv file of it.
    data = []

    for card in project_cards:
        try:
            title_element = card.find_element(By.CLASS_NAME, "JobSearchCard-primary-heading-link")
            title = title_element.text
            link = title_element.get_attribute("href")
        except:
            title = None
            link = None
        
        try:
            days_left_element = card.find_element(By.CLASS_NAME, "JobSearchCard-primary-heading-days")
            days_left = days_left_element.text
        except:
            days_left = None
        
        try:
            description_element = card.find_element(By.CLASS_NAME, "JobSearchCard-primary-description")
            description = description_element.text if description_element else ''
        except:
            description = None
        
        try:
            tags_elements = card.find_elements(By.CLASS_NAME, "JobSearchCard-primary-tagsLink")
            tags = [tag.text for tag in tags_elements]
        except:
            tags = None
        
        data.append([title, link, days_left, description, ", ".join(tags)])
    
    return data
# making CSV file of data.
def write_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Days Left", "Description", "Tags"])
        writer.writerows(data)

if __name__ == "__main__":
    USERNAME = 'XXXXXXXX'
    PASSWORD = 'XXXXXXXXX'
    LOGIN_URL = 'https://www.freelancer.in/login'

    
    URL = 'https://www.freelancer.in/search/projects?projectLanguages=hi,en&projectSkills=6,13,95,292,305,320,761,2607&projectSort=oldest'
    CSV_FILE = "project_details.csv"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
# calling all functions

    try:
        driver = login_to_freelancer(USERNAME, PASSWORD, LOGIN_URL)
        data = scrape_projects(URL)
        write_to_csv(data, CSV_FILE)
        print(f"Data has been written to {CSV_FILE}")
    finally:
        driver.quit()
