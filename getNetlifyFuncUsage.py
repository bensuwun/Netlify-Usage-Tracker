import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class NetlifyTracker:
    def __init__(self, email, password, sitenames, webhook_url):
        self.email = email
        self.password = password
        self.sitenames = sitenames
        self.webhook_url = webhook_url
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
        self.data = {
            "usages": []
        }

    """
        Direct browser to login page, inputs given username and password.
    """
    def login(self):
        # Go to base URL
        self.driver.get("https://app.netlify.com")

        emailButton = self.driver.find_element(By.NAME, "email")
        emailButton.click()

        # Input login details
        try:
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            # Get email, password input fields
            inputFields = form.find_elements(By.TAG_NAME, "input")

            # Input credentials and submit
            inputFields[0].send_keys(self.email)
            inputFields[1].send_keys(self.password)
            
            form.submit()

        except Exception as e:
            print(e)

    """
        Navigates to given site name to access its settings.
        @param sitename - string indicating site name in Netlify
    """
    def navigateToFunctionUsage(self, sitename, isFirstIter):
        try:
            print("Navigating to {}".format(sitename))
            # Wait for login to finish
            if isFirstIter:
                siteLink = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, sitename))
                )
            self.driver.get("https://app.netlify.com/sites/{}/settings/functions".format(sitename))
        except Exception as e:
            print("Error navigating to site")
            print(e)


    """
        Extracts the current usage of the given site.
        @param sitename - string name of the site
    """
    # Reference: https://stackoverflow.com/questions/29772457/webdriver-select-element-that-has-before
    #          : https://www.lambdatest.com/blog/handling-pseudo-elements-in-css-with-selenium/
    #          : https://selenium-python.readthedocs.io/waits.html
    def extractFunctionUsage(self, sitename):
        try:
            section_overview = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "section-overview"))
            )
            
            timeframeElement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "usage"))
            )

            usage = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".fit.subdued"))
            )

            # Implicit wait for content to load
            self.driver.implicitly_wait(4)
            
            # Get usages
            usageElements = section_overview.find_elements(By.CSS_SELECTOR, ".fit.subdued")
            
            # Last updated
            headerInfoElements = section_overview.find_elements(By.CLASS_NAME, "table-header")
            lastUpdatedElements = headerInfoElements[0].find_elements(By.TAG_NAME, "div")

            currentPlan = lastUpdatedElements[0].text
            timeframe = timeframeElement.text
            currentRequests = usageElements[0].text.split("\n")[0]
            currentRuntime = usageElements[1].text.split("\n")[0]
            
            # Display information
            print("Last updated: {}".format(currentPlan))
            print("Date Range: {}".format(timeframe))
            print("Current Requests: {}".format(currentRequests))
            print("Current Runtime: {}".format(currentRuntime))

            usageInfo = {
                "sitename": sitename,
                "currentPlan": currentPlan,
                "timeframe": timeframe,
                "currentRequests": currentRequests,
                "currentRuntime": currentRuntime
            }

            return usageInfo
            
        except Exception as e:
            print("Error extracting function usage")
            print(e)

    """
        Main runner function for class. 
        Used to traverse all the sites listed in sitenames
        @param sendToWebhook - boolean to determine if data collected will be sent to webhook
    """
    def track(self, sendToWebhook):
        self.login()

        for i in range(len(self.sitenames)):
            isFirstIter = True if i == 0 else False
            self.navigateToFunctionUsage(self.sitenames[i], isFirstIter)

            usage = self.extractFunctionUsage(self.sitenames[i])
            
            self.data["usages"].append(usage)

        print("Raw payload:")
        print(self.data["usages"])
        
        if sendToWebhook:
            # Generate POST request
            try:
                response = requests.post(url = self.webhook_url.encode(), json = self.data)
                print(response.status_code)
                print(response.raw)
            except Exception as e:
                print("Failed to send POST request")
                print(e)

        self.driver.quit()

def main():
    # Initialize NetlifyTracker
    sitenames = ["staging-dlsuuxsoc", "dlsuuxsoc"]
    webhook_url = os.environ.get("WEBHOOK_URL")
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")

    tracker = NetlifyTracker(email, password, sitenames, webhook_url)

    tracker.track(sendToWebhook = True)
    
if __name__ == "__main__":
    main()

