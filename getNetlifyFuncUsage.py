from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

load_dotenv()

"""
    Direct browser to login page, inputs given username and password.
"""
def login():
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    emailButton = driver.find_element(By.NAME, "email")
    emailButton.click()

    # Input login details
    try:
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        # Get email, password input fields
        inputFields = form.find_elements(By.TAG_NAME, "input")

        # Input credentials and submit
        inputFields[0].send_keys(email)
        inputFields[1].send_keys(password)
        
        form.submit()

    except Exception as e:
        print(e)

"""
    Navigates to given site name to access its settings.
    @param sitename - string indicating site name in Netlify
"""
def navigateToFunctionUsage(sitename):
    try:
        siteLink = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, sitename))
        )
        driver.get("https://app.netlify.com/sites/{}/settings/functions".format(sitename))
    except Exception as e:
        print("Error navigating to site")
        print(e)


"""
    Extracts the current usage of the site.
"""
# Reference: https://stackoverflow.com/questions/29772457/webdriver-select-element-that-has-before
        #          : https://www.lambdatest.com/blog/handling-pseudo-elements-in-css-with-selenium/
        #          : https://selenium-python.readthedocs.io/waits.html
def extractFunctionUsage():
    try:
        section_overview = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "section-overview"))
        )
        
        timeframeElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "usage"))
        )

        usage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fit.subdued"))
        )

        # Implicit wait for content to load
        driver.implicitly_wait(4)
        
        # Get usages
        usageElements = section_overview.find_elements(By.CSS_SELECTOR, ".fit.subdued")
        
        # Last updated
        headerInfoElements = section_overview.find_elements(By.CLASS_NAME, "table-header")
        lastUpdatedElements = headerInfoElements[0].find_elements(By.TAG_NAME, "div")

        currentPlan = lastUpdatedElements[0].text
        timeframe = timeframeElement.text
        currentRequests = usageElements[0].text.split("\n")[0]
        currentRunTime = usageElements[1].text.split("\n")[0]
        
        # Display information
        print("Last updated: {}".format(currentPlan))
        print("Date Range: {}".format(timeframe))
        print("Current Requests: {}".format(currentRequests))
        print("Current Runtime: {}".format(currentRunTime))

        usageInfo = {
            "currentPlan": currentPlan,
            "timeframe": timeframe,
            "currentRequests": currentRequests,
            "currentRunTime": currentRunTime
        }

        return usageInfo
        
    except Exception as e:
        print("Error extracting function usage")
        print(e)

# Setup Chrome webdriver
sitename = os.environ.get("SITENAME")
webhook_url = os.environ.get("WEBHOOK_URL")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)

# Go to base URL
driver.get("https://app.netlify.com")

# Check if not yet logged in
try:
    loginHeader = driver.find_element(By.CLASS_NAME, "page-header")

    # Login first
    login()
    
    # Navigate to function usage of specific site/repo
    navigateToFunctionUsage(sitename)

    # Extract usage
    usageInfo = extractFunctionUsage()
    usageInfo["site"] = sitename

    # Generate POST request
    try:
        response = requests.post(url = webhook_url.encode(), data = usageInfo)
        print(response.status_code)
        print(response.raw)
    except Exception as e:
        print("Failed to send POST request")
        print(e)

    driver.quit()

except Exception as e:
    print("App not found")
    print(e)
