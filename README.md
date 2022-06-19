# Netlify Usage Tracker
This project was inspired due to Netlify autoupdating their pricing plans when a site goes beyond the free usage limit.

_Powered by Selenium WebDriver_

---

Netlify Usage Tracker (NeUT) is an automation script to help track current netlify function usage of your sites and allows optional integration to a webhook URL for exporting. 
NeUT will scrape your sites' current Netlify Function usage (i.e. requests, runtime) so you will no longer have to manually check them yourself. It is helpful if you want to avoid going beyond your plan's limits. 

Note: You will need to have access to the account's username and password in order to access a site's usage.

## Guide
After forking, setup the following environment secrets in your repository's settings.

| Key | Value |
| --- | ----- |
| EMAIL | \<email in Netlify\> |
| PASSWORD | \<password in Netlify\> |
| WEBHOOK_URL | \<URL of webhook to send POST request to\>

Github actions will then proceed to run the script at some time around 12 PM UTC using the .yml file.

## Sample Output from Discord Webhook
![image](https://user-images.githubusercontent.com/59037332/174475451-0e6ae081-31af-46f5-9e81-431e3b69cb6d.png)
 
## Dependencies
- selenium
- webdriver_manager
- requests

## Plans
- As of current implementation, sitenames to track are currently static. Can refactor as a GET request to a DB, store the DB url in secrets, and run the request to make it dynamic.
- Can only track a single user's sites, can refactor to scale to multiple users in consideration for those who have sites in multiple accounts
