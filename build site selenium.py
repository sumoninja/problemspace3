# build.com selenium


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

link = "https://www.build.com/delta-9159-dst/s380199?uid=2794656"
driver.get(link)
time.sleep(5)

print(driver.title)

# open up reviews expandable
expand = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[3]/section[3]/div/div/div[2]/div/div/div[1]/div")
expand.click()

# find element by link text
reviews = driver.find_element_by_id("review-content")

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

