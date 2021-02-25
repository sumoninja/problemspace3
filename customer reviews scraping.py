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
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

print("Hello world!")


#simple storage class to make the organization of review data a little bit easier

class Review(object):
	def __init__(self, review_id, review_date, review_text, star_rating, response_date, response_text, resolution_date, resolution_text, has_response, has_resolution):
		self.review_date = review_date #string
		self.review_id = review_id
		self.review_text = review_text #string
		self.star_rating = star_rating #integer
		self.response_date = response_date #string
		self.response_text = response_text #string
		self.resolution_date = resolution_date #string
		self.resolution_text = resolution_text #string
		self.has_response = has_response #boolean
		self.has_resolution = has_resolution #boolean

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

def scrape_single_page(driver):
	page_source = driver.page_source
	#print(page_source)
	soup = bs.BeautifulSoup(page_source, 'lxml')

	reviews = soup.find_all('div', class_='rvw js-rvw')

	for review in reviews:
		#These are the fields we will be scraping
		review_id = review['id']
		review_date = None
		review_text = ""
		star_rating = ""
		response_date = None
		response_text = ""
		resolution_date = None
		resolution_text = ""

		review_body = review.find('div', class_='rvw-bd')
		review_dates = review_body.find_all('span', class_='ca-txt-cpt')
		for review_date in review_dates:
			if 'Resolution' in review_date.text:
				resolution_date = review_date.text
			elif 'Original review' in review_date.text:
				review_date = review_date.text

		try:
			star_rating_tag = review.find('meta', itemprop="ratingValue")
			star_rating = star_rating_tag['content']
		except Exception as e:
			star_rating = ""

		all_paragraph_tags = review_body.find_all('p')
		for raw_review_text in all_paragraph_tags:
			if len(raw_review_text.text) > 0:
				review_text = review_text + raw_review_text.text
				
		review_resolved = review_body.find('div', class_='rvw-bd__csmr-resp')
		if review_resolved is not None:
			raw_resolution_text = review_resolved.find_all('p')
			for resolution_text_item in raw_resolution_text:
				if len(resolution_text_item.text) > 0:
					resolution_text = resolution_text + resolution_text_item.text

		company_response = review.find('div', class_="rvw-comp-resp rvw-comp-resp--no-shield")
		if company_response is not None:
			response_time = company_response.find('time', class_="ca-txt--clr-gray")
			response_date = response_time['datetime']
			raw_response_text = company_response.find_all('p')
			for text_item in raw_response_text:
				if len(text_item.text) > 0:
					response_text = response_text + text_item.text

		print("REVIEW DATA: ======================================================================================")
		print("		Review ID: " + review_id)
		if review_date is not None:
			print("		Review date: " + review_date)
		else:
			print("		Review date: None")
		print("		Star rating: " + star_rating)
		print("		Review text: " + review_text)
		if response_date is not None:
			print("		Response date: " + response_date)
		else:
			print("		Response date: None")
		print("		Response text: " + response_text)
		if resolution_date is not None:
			print("		Resolution date: " + resolution_date)
		else:
			print("		Resolution date: None")
		print("		Resolution text: " + resolution_text)


def main():
	search_url = 'https://www.consumeraffairs.com/homeowners/delta-faucets.html?#sort=recent&filter=none'

	chrome_options = Options()
	chrome_options.headless = True

	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get(search_url)

	time.sleep(10)

	found_button = True
	num_iterations = 0
	while num_iterations < 5: #We want to scrape until we can no longer find the "next page" button onscreen, which is when we know there are no more results
		print("ITERATION NUMBER " + str(num_iterations))
		
		if num_iterations == 0:

			#Explanation: We need to scroll down the first page of result to load all of them. Subsequent pages will have all their results loaded
			#if we do this, so we only need to scroll down on the first page.

			driver.execute_script("window.scrollTo(0,9000)")
			time.sleep(5)
			driver.execute_script("window.scrollTo(0,16000)") #These pieces of code scroll the page down, since new reviews only load once the page has been
			#scrolled far enough
			time.sleep(5)
		else:
			driver.execute_script("window.scrollTo(0, 1000)")

		time.sleep(5) #Let the page load before we scrape it

		#Scraping done in this method, defined above	
		scrape_single_page(driver)
		
		time.sleep(5)

		#This code attempts to find the button to go to the next page and clicks it 
		try:
			if num_iterations == 0:
				next_page_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/div/div[3]/div/nav/a')
			else:
				next_page_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/div/div[3]/div/nav/a[2]') 
			print(next_page_button)
			found_button = True
			print("Found the button")
			print("**********************************************************NEXT PAGE RESULTS START HERE************************************************")
			next_page_button.click()
		except Exception as e:
			print(e)
			print("Couldn't find the button")
			found_button = False
		num_iterations += 1
		time.sleep(10)

#Call the main() function

main()

'''
Page 3 to page 4: /html/body/main/div[1]/div/div/div[3]/div/nav/a
Page 4 to page 5: /html/body/main/div[1]/div/div/div[3]/div/nav/a[2]
Page 5 to page 6: /html/body/main/div[1]/div/div/div[3]/div/nav/a[2]
Page 6 to page 7: /html/body/main/div[1]/div/div/div[3]/div/nav/a[2]
Page 7 to page 8: N/A
'''