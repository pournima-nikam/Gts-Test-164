from selenium import webdriver
from selenium.webdriver.common.by import By
import time



def chromedriver():
    browser = webdriver.Chrome('C:\\Translation EXE\\chromedriver.exe')
    browser.get('https://simap.org.pk/member-directory/')
    browser.maximize_window()
    time.sleep(2)
    navigation(browser)
    
    
def navigation(browser):
    
    for submit in browser.find_elements(By.XPATH,'//*[@class="elementor-widget-container"]/div/form/div/ul/li[3]/input[2]'):
        submit.click()
        time.sleep(2)
        break
    
    collected_list = []
    count = 1
    error = True
    while error == True:
        for _ in browser.find_elements(By.XPATH,'//*[@id="main"]/div/article/div/div/header/h2/a'):
            for link in browser.find_elements(By.XPATH,'//*[@id="main"]/div/article['+str(count)+']/div/div/header/h2/a'):
                company_href = link.get_attribute('href')
                company_name = link.get_attribute('innerText').strip()
                print(company_href,company_name)
                collected_list.append(company_href+'*******'+company_name)
            count += 1
        for next in browser.find_elements(By.CLASS_NAME,"nav-links"):  
            next_html = next.get_attribute('outerHTML')  
        if "Next Page" in next_html:    
            for next_page in browser.find_elements(By.XPATH,'//*[@id="primary"]/div/nav/div/a'):
                next_page_href = next_page.get_attribute('href')
                next_page_text = next_page.get_attribute('innerText')
                if "Next Page →" in next_page_text:    
                    next_page.click()
                    # browser.get(next_page_href)
                    time.sleep(2)
                    count = 1
                    error = True
                else:
                    error = False
        else:
            error = False 
    
            
        
chromedriver()