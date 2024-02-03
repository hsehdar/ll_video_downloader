import random,time,os,sys,logging,platform
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
base_directory = '/srv/backups/LinkedIn Learning/'
play_video = False
download_video = False
course_title = 'Course title'
course_instructor = 'Course instructor'
section_title = 'Section title'
section_max_number = 0
item_number = 1

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

time.sleep(round(random.uniform(3,4),2))

try:
	driver.find_element(By.XPATH, '//div[@class="classroom-nav__details"]/h1').text
except:
	if driver.find_element(By.XPATH, '//div[@class="course-overview-toc"]/..//li/a/span[contains(@class, "-text")]').text == 'Locked content':
		download_video = False
	driver.find_elements(By.XPATH, '//div[@class="course-overview-toc"]//a[1]')[0].click()

time.sleep(round(random.uniform(3,4),2))

try:
	driver.find_element(By.XPATH, '//button[@class="vjs-play-control vjs-control vjs-button vjs-playing"]').click()
except:
	print('Video is not playing')

time.sleep(round(random.uniform(2,3),2))

driver.find_element(By.XPATH, '//div[@id="linkedin-learning-captions-menu-toggle"]').click()
try:
	driver.find_element(By.XPATH, '//li[.="Off"]').click()
except:
	driver.find_element(By.XPATH, '//div[@id="linkedin-learning-captions-menu-toggle"]').click()
	print('Captions are off')

time.sleep(round(random.uniform(2,3),2))

if driver.find_element(By.XPATH, '//button[starts-with(@class, "vjs-mute-control")]').text == 'Unmute':
	driver.find_element(By.XPATH, '//button[starts-with(@class, "vjs-mute-control")]').click()

time.sleep(round(random.uniform(2,3),2))

try:
	course_title = driver.find_element(By.XPATH, '//div[@class="classroom-nav__details"]/h1').text
except:
	print('Unable to fetch course title')

base_directory = base_directory + course_title
del course_title

try:
	course_instructor = driver.find_element(By.XPATH, '//div[starts-with(@class, "instructor__name ")]').text
except:
	print('Unable to fetch course instructor')

base_directory = base_directory + ' by ' + course_instructor
del course_instructor

for item in driver.find_elements(By.XPATH, '//div[@class="classroom-layout-sidebar-body classroom-layout__sidebar-body hue-web-color-scheme--dark classroom-body__sidebar-body"]/section'):
	if item.find_element(By.XPATH, './h2/button').text[0].isdigit() and section_max_number != item.find_element(By.XPATH, './h2/button').text.partition('. ')[0]:
		section_max_number = item.find_element(By.XPATH, './h2/button').text.partition('. ')[0]

for item in driver.find_elements(By.XPATH, '//div[@class="classroom-layout-sidebar-body classroom-layout__sidebar-body hue-web-color-scheme--dark classroom-body__sidebar-body"]//button'):
	if item.get_attribute("aria-expanded") == 'false':
		item.click()

def get_current_position_of_video():
	try:
		return float(driver.find_element(By.XPATH, '//div[@class="vjs-progress-holder vjs-slider vjs-slider-horizontal"]').get_attribute('aria-valuenow'))
	except:
		print('Unable to fetch the current video position')

def get_full_screen_status():
    try:
        return driver.find_element(By.XPATH, '//button[@class="vjs-fullscreen-control vjs-control vjs-button"]').text
    except:
        print('Unable to get full screen status')

for item in driver.find_elements(By.XPATH, '//div[@class="classroom-layout-sidebar-body classroom-layout__sidebar-body hue-web-color-scheme--dark classroom-body__sidebar-body"]//ul/li[contains(@data-toc-content-id,"learningApiVideo")]/a'):
	item.click()
	time.sleep(round(random.uniform(3,4),2))
	section_title_previous = section_title
	section_title = item.find_element(By.XPATH, './../../../h2/button').text.replace('. ', ' ').replace('Introduction', '0 Introduction').replace('Conclusion', str(int(section_max_number)+1) + ' Conclusion')

	if (section_title_previous != section_title):
		item_number = 1

	video_title = 'Video title'
	try:
		video_title = item.find_element(By.XPATH, './/div[contains(@class,"classroom-toc-item__title")]').text.partition('\n')[0]
	except:
		print('Unable to fetch video title')

	video_local_file = base_directory + '/' + section_title + '/' + f'{item_number:02d} ' + video_title + '.mp4'

	if not play_video:
		try:
			driver.find_element(By.XPATH, '//button[@class="vjs-play-control vjs-control vjs-button vjs-playing"]').click()
		except:
			print('Video "'+ f'{item_number:02d} ' + video_title + '" is not playing in the section "' + section_title + '"')

	video_url = 'LINK'
	try:
		video_url = (driver.find_element(By.XPATH, '//video').get_attribute("src"))
	except:
		print('Video "' + f'{item_number:02d} ' + video_title + '" is locked in the section "' + section_title + '"')

	if not download_video:
		if platform.system() == 'Linux':
			download_shell_file_path = base_directory + '/download.sh'
		elif platform.system() == 'Windows':
			download_shell_file_path = base_directory + '/download.bat'
		if not os.path.exists(os.path.dirname(download_shell_file_path)):
			os.makedirs(os.path.dirname(download_shell_file_path))
		if os.path.exists(download_shell_file_path):
			append_write = 'a'
		else:
			append_write = 'w'
		download_shell_file = open(download_shell_file_path, append_write)
		download_shell_file.write('curl -# --create-dirs -kLo "' + video_local_file + '" "' + video_url + '";' + '\n')
		download_shell_file.close()

	if download_video:
		if not os.path.exists(os.path.dirname(video_local_file)):
			os.makedirs(os.path.dirname(video_local_file))
		urlretrieve(video_url, video_local_file)

		try:
			driver.find_element(By.XPATH, '//button[@data-live-test-classroom-layout-tab="TRANSCRIPT"]').click()
		except:
			print('Unable to view transcript for the video "' + f'{item_number:02d} ' + video_title + '" is locked in the section "' + section_title + '"')
		transcript_file_path = video_local_file.replace('.mp4', '.txt')
		transcript_file = open(transcript_file_path, 'w')
		transcript_file.write(driver.find_element(By.XPATH, '//div[@class="classroom-transcript__lines"]').text.replace('. ', '.\n').replace('? ', '?\n'))
		transcript_file.close()
		if play_video and "#check-small" not in item.get_attribute('innerHTML'):
			try:
				driver.find_element(By.XPATH, '//button[@class="vjs-play-control vjs-control vjs-button vjs-paused"]').click()
			except:
				print('Video "' + f'{item_number:02d} ' + video_title + '" is playing in the section "' + section_title + '"')

			current_position = get_current_position_of_video()
			while not current_position >= float(99.99):
				current_position = get_current_position_of_video()
			try:
				driver.find_element(By.XPATH, '//button[@class="vjs-play-control vjs-control vjs-button vjs-playing"]').click()
			except:
				print('Video "' + f'{item_number:02d} ' + video_title + '" was not playing in the section "' + section_title + '"')

	time.sleep(round(random.uniform(1,2),2))
	item_number += 1

driver.close()
driver.quit()
linkedin_learning_url_file = open(base_directory + '/url.txt', 'w')
linkedin_learning_url_file.write(linkedin_learning_url)
linkedin_learning_url_file.close()
sys.exit()
