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

print("Hello world!")

search_url = 'https://www.consumeraffairs.com/homeowners/delta-faucets.html?#sort=recent&filter=none'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(search_url)

time.sleep(10)

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

print("Made it here")

page_source = driver.page_source
#print(page_source)
soup = bs.BeautifulSoup(page_source, 'lxml')

reviews = soup.find_all('div', class_='rvw js-rvw')

for review in reviews:
	print("Found a review ==============================================================================================")
	review_body = review.find('div', class_='rvw-bd')
	all_paragraph_tags = review_body.find_all('p')
	for review_text in all_paragraph_tags:
		if len(review_text.text) > 0:
			print("REVIEW TEXT:")
			print(review_text.text)
	review_resolved = review.find('div', class_='rvw-bd__csmr-resp')
	if review_resolved is not None:
		review_resolved_text = review_resolved.find_all('p')
		for text_item in review_resolved_text:
			if len(text_item.text) > 0:
				print("RESOLVED MESSAGE:")
				print(text_item.text)
	delta_faucet_response = review_body.find_all('div', class_='rvw-comp-resp__txt')
	if len(delta_faucet_response) > 0:
		for item in delta_faucet_response:
			response_text = delta_faucet_response[0].find('p')
			print("RESPONSE TEXT:")
			print(response_text.text)


