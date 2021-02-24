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
	soup = bs.BeautifulSoup(page_source, "lxml")
	review_div = soup.find("div", class_="listing-container review-item-container")
	reviews = review_div.find_all("div", itemprop="review")
	for review in reviews:
		review_id = review["id"]
		date_prop = review.find("meta", itemprop="datePublished")
		date = date_prop['content']
		
		star_rating = None
		try:
			star_rating_div = review.find("div", class_="stars")
			star_rating = star_rating_div["data-active-count"]
		except Exception as e:
			print("Couldn't find stars for this particular rating")


		review_text_div = review.find("div", itemprop="reviewBody")
		review_text = review_text_div.text

		split_review_text = review_text.split()
		review_text_no_spaces = " ".join(split_review_text)

		print(review_id)
		print(date)
		print(star_rating)
		print(review_text_no_spaces)

def main():
	search_url = 'https://delta-faucet.pissedconsumer.com/review.html'

	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get(search_url)

	time.sleep(10)

	button_found = True

	num_iterations = 0
	while button_found:
		scrape(driver)
		time.sleep(5)
		try:
			if num_iterations == 0:
				xpath = "/html/body/div[4]/div[4]/div/div[5]/ul/li[9]/a"
			elif num_iterations == 1 or num_iterations == 2 or num_iterations == 9 or num_iterations == 10:
				xpath = "/html/body/div[4]/div[4]/div/div[3]/ul/li[9]/a"
			else: 
				xpath = "/html/body/div[4]/div[4]/div/div[3]/ul/li[11]/a"
			next_button = driver.find_element_by_xpath(xpath) 
			print("MOVING TO THE NEXT PAGE ===================================================================")
			next_button.click()
			button_found = True
			num_iterations += 1
		except Exception as e:
			print(e)
			button_found = False
			break
		time.sleep(10)

'''
page 1 to page 2: /html/body/div[4]/div[4]/div/div[5]/ul/li[9]/a n = 0
page 2 to page 3: /html/body/div[4]/div[4]/div/div[3]/ul/li[9]/a n = 1
page 3 to page 4: /html/body/div[4]/div[4]/div/div[3]/ul/li[9]/a n = 2
page 4 to page 5: /html/body/div[4]/div[4]/div/div[3]/ul/li[11]/a n = 3 
page 5 to page 6: /html/body/div[4]/div[4]/div/div[3]/ul/li[11]/a n = 4
page 6 to page 7: /html/body/div[4]/div[4]/div/div[3]/ul/li[11]/a n = 5
page 7 to page 8: /html/body/div[4]/div[4]/div/div[3]/ul/li[11]/a n = 6
'''

main()



