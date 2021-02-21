import selenium
import bs4 as bs
import urllib.request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

print("Hello world!")

search_url = 'https://www.consumeraffairs.com/homeowners/delta-faucets.html?#sort=recent&filter=none'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(search_url)

time.sleep(10)


#This code closes a popup that sometimes appears onscreen. I'm not sure if it's still needed, since I think the popup will only
#appear if you move your mouse on the webpage, and obviously we won't be doing any of that
'''
successfully_closed_popup = False
while successfully_closed_popup == False:
	try:
		popup_button_no_thanks = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/form/div/div/button[2]')
		popup_button_no_thanks.click()
		print("Successfully closed the popup")
		successfully_closed_popup = True
	except Exception as e:
		if not successfully_closed_popup:
			print(e)
			print("The popup has not appeared yet")
			time.sleep(30)
'''

#simple storage class to make the organization of review data a little bit easier

class Review(object):
	def __init__(self, review_date, review_text, response_date, response_text, resolution_date, resolution_text):
		self.review_date = review_date
		self.review_text = review_text
		self.response_date = response_date
		self.response_text = response_text
		self.resolution_date = resolution_date
		self.resolution_text = resolution_text

	def convert_raw_date_to_datetime_obj(self, raw_string):
		if raw_string is None:
			return None
		else:
			string_to_convert_list = raw_string.split(" ")

			month = string_to_convert_list[-3]
			day = string_to_convert_list[-2]
			year = string_to_convert_list[-1]
			date_string = month[0:len(month) - 1] + " " + day[0:len(day) - 1] + " " + year
			datetime_obj = datetime.strptime(date_string, '%b %d %Y')
			return datetime_obj

driver.execute_script("window.scrollTo(0,9000)")
time.sleep(5)
driver.execute_script("window.scrollTo(0,16000)") #These pieces of code scroll the page down, since new reviews only load once the page has been
#scrolled far enough
time.sleep(5)


#This code is WIP. It finds the button to go to the next page of reviews and clicks it.
'''
try:
	next_page_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/div/div[3]/div/nav/a')
	print(next_page_button)
	next_page_button.click()
	print("Found the button")
except Exception as e:
	print(e)
	print("Couldn't find the button")

'''
print("Made it here")

page_source = driver.page_source
#print(page_source)
soup = bs.BeautifulSoup(page_source, 'lxml')

reviews = soup.find_all('div', class_='rvw js-rvw')

for review in reviews:

	review_date = None
	review_text = ""
	response_date = None
	response_text = ""
	resolution_date = None
	resolution_text = ""

	print("Found a review ==============================================================================================")
	review_body = review.find('div', class_='rvw-bd')
	review_dates = review_body.find_all('span', class_='ca-txt-cpt')
	for review_date in review_dates:
		if 'Resolution' in review_date.text:
			resolution_date = review_date.text
		elif 'Original review' in review_date.text:
			review_date = review_date.text

	all_paragraph_tags = review_body.find_all('p')
	for raw_review_text in all_paragraph_tags:
		if len(raw_review_text.text) > 0:
			print("REVIEW TEXT:")
			print(raw_review_text.text)
			review_text = review_text + raw_review_text.text

	review_resolved = review_body.find('div', class_='rvw-bd__csmr-resp')
	if review_resolved is not None:
		raw_resolution_text = review_resolved.find_all('p')
		for resolution_text_item in raw_resolution_text:
			if len(resolution_text_item.text) > 0:
				print("RESOLUTION TEXT:")
				print(resolution_text_item.text)
				resolution_text = resolution_text + resolution_text_item.text

	company_response = review.find('div', class_="rvw-comp-resp rvw-comp-resp--no-shield")
	if company_response is not None:
		response_time = company_response.find('time', class_="ca-txt--clr-gray")
		print("RESPONSE TIME:")
		print(response_time['datetime'])
		response_date = response_time['datetime']
		raw_response_text = company_response.find_all('p')
		for text_item in raw_response_text:
			if len(text_item.text) > 0:
				print("RESPONSE TEXT:")
				print(text_item.text)
				response_text = response_text + text_item.text

	


