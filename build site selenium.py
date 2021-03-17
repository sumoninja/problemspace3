# build.com selenium

#PLEASE READ THE BOTTOM

import selenium
from webdriver_manager.chrome import ChromeDriverManager #if you do not have this library please install it using pip. It will automatically download 
#the latest webdriver so that you don't have to manually do it yourself.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(ChromeDriverManager().install())

link = "https://www.build.com/delta-9159-dst/s380199?uid=2794656"
driver.get(link)
time.sleep(5)

print(driver.title)

close_popup_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div/div/div/div/div[1]/div") #this code finds the button to close that annoying popup and clicks it
close_popup_button.click()

time.sleep(5)

# open up reviews expandable
#expand = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[3]/section[3]/div/div/div[2]/div/div/div[1]/div") 

expand = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/section[4]/div[2]/section") #this code finds the button to expand the reviews section

#print(expand)


#button = driver.find_element_by_xpath("/html/body/div[2]/div/main/div[1]/section[4]/div[2]/section/div[1]")

#print(button)


expand.click() #this code clicks the button to expand the reviews section

time.sleep(5)

# find element by link text
#reviews = driver.find_element_by_id("review-content")

reviews = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/section[4]/div[2]/section/div[3]/div/div/div/div/div/div/ol") #the reviews in the reviews section
#are stored in an unordered list HTML tag. This code finds that unordered list.


time.sleep(5)

more_reviews_button = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/section[4]/div[2]/section/div[3]/div/div/div/div/div/div/div[4]/div/button")
#there is also a button to load more reviews. This code finds the button and the code directly below clicks on it


more_reviews_button.click()

time.sleep(5)

individual_reviews = reviews.find_elements_by_tag_name("li")
#within that unordered list we found above, this line finds all elements with the tag <li>. A <li> tag represents an item in an <ol> (unordered list) tag.
#so we're basically just finding all the reviews in the list.

print("Attempting to access individual reviews...")

for review in individual_reviews: #iterate through all the reviews we found
	paragraphs = review.find_elements_by_tag_name("p") #within each review, find a <p> tag.
	for p in paragraphs: #for each paragraph tag, print its text.
		print(p.text)


#####################################################################
'''
WHAT I NEED YOU TO DO:
1. Put this code in a function
2. Currently, the code to find <p> tags in each review will return all the <p> tags. Try and sort them into review text, response from the company,
etc. 

3. Make it so that the more reviews button will get clicked multiple times because clicking it once won't load all of the 200+ reviews. Maybe try using
a for loop or something.

4. Try to get other elements from each review, i.e. number of stars, text, etc

5. The function should return a list of dicts, where each dict has the following information:

mydict  = {
			"review id": <review_id>,
			"review date": <date>,
			"review text": <review_text>,
			"star rating": <star rating>,
			"response date": <date>,
			"response text": <text>,
			"resolution date": <date>,
			"resolution text": <text>
		}

If you're short on time, try to just find the review text, date, and star rating. 

As always, ask if you have any questions. 
'''
#####################################################################



'''
for ind_review in reviews.find_element_by_class_name("bv-content-review"):
    stars = ind_review.find_element_by_class_name("bv-rating-stars-on")
    stars = stars.find_element_by_tag_name("span")
    stars = stars.get_attribute("style")
    stars = stars.split(" ")[1]
    print(stars)

    review_title = reviews.find_element_by_class_name("bv-content-title").text
    print(review_title)

    review_content = reviews.find_element_by_class_name("bv-content-summary-body").text
    print(review_content)

# open more reviews through load more button
load_more = driver.find_element_by_class_name("bv-content-btn-pages-load-more-text")
load_more.click()

print("Done")
'''

