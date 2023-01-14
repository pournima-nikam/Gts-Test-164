from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from datetime import datetime




def chromedriver():
    browser = webdriver.Chrome('/home/gts-anil/anil exe/Translation Exe/chromedriver') #chromedriver path
    browser.get('https://muasamcong.mpi.gov.vn/en/contractor-selection?infoType=6&fromD=&toD=&inputParam=') #website
    browser.maximize_window()
    time.sleep(2)
    navigation(browser)

def navigation(browser):
    for link in browser.find_elements(By.XPATH,'//*[@id="other-tbmt"]/div/div[2]/div/div/div[3]/div[1]/div/div[2]/div/div[1]/div/div[1]/a/h5'):
        link.click()
        time.sleep(2)
    browser.back()
    time.sleep(20)


chromedriver()