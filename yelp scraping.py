import json
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

def scrape(driver):
	page_source = driver.page_source
	#print(page_source)
	soup = bs.BeautifulSoup(page_source, "lxml")
	
	#print(soup)

	data_script = soup.find('script', type="application/ld+json") #we're literally just directly getting the json from the backend instead of scraping the front end.
	#print(data_script.string)

	data_json = json.loads(data_script.string)

	#print(data_json)

	print(data_json['@context'])

	reviews = data_json['review']

	for review in reviews:
		print("AUTHOR: " + review['author'])
		print("DATE PUBLISHED: " + review['datePublished'])
		print("REVIEW RATING: " + "".join(str(review['reviewRating']['ratingValue']).split()))
		print("REVIEW TEXT: " + review['description'])

	#reviews_list = soup.find('ul', class_=' undefined list__373c0__3GI_T')
	#print(reviews_list)
	#reviews = reviews_list.find('li', class_=' margin-b5__373c0__2ErL8 border-color--default__373c0__3-ifU')
	#for review in reviews:
	#	print("Found a review")

	# <div class="main-content-wrap main-content-wrap--full"> 

def main():
	search_url = 'https://www.yelp.com/biz/delta-faucet-company-indianapolis?sort_by=date_desc'
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get(search_url)

	time.sleep(5)

	scrape(driver)

	time.sleep(30)



main()