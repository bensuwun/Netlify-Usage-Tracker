# Netlify Usage Tracker
This project was inspired due to Netlify autoupdating their pricing plans when a site goes beyond the free usage limit.

Netlify Usage Tracker (NET) is an automation script to help track current netlify function usage of your sites and allows optional integration to a webhook URL for exporting. 
NET will scrape your sites' current Netlify Function usage (i.e. requests, runtime) so you will no longer have to manually check them yourself. It is helpful if you want to avoid going beyond your plan's limits. 

Note: You will need to have access to the account's username and password in order to access a site's usage.

## Dependencies
- selenium
- webdriver_manager
- requests
- os

## Plans
- Setup yaml file for scheduled execution
