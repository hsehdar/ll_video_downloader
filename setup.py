import random,time,os,sys,logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlretrieve

linkedin_learning_url = 'https://www.linkedin.com/learning/implementing-the-nist-privacy-framework'
chrome_data_dir = '/srv/backups/ChromeDataDir'

os.environ['WDM_LOG_LEVEL'] = '0'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--enable-new-usb-backend")
chrome_options.add_argument("--test-type")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--user-data-dir=" + chrome_data_dir)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(linkedin_learning_url)
linkedin_logged_in = False
try:
	driver.find_element(By.XPATH, '//a[contains(text(), "Sign in")]').text
except:
	linkedin_logged_in = True

if linkedin_logged_in:
	print('You have already logged into LinkedIn Learning')
else:
	driver.execute_script('alert("Log in to LinkedIn within next 5 minutes")')
	time.sleep(300)
driver.close()
driver.quit()
sys.exit()