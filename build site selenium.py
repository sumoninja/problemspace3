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

# dropdown menu
drop_down = reviews.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[3]/section[3]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div[2]/div[4]/div[3]/div")
hover = ActionChains(driver).move_to_element(drop_down)
hover.perform()


most_helpful = drop_down.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[3]/section[3]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div[2]/div[4]/div[3]/div/select/option[2]")
most_helpful.click()



print("Done")

