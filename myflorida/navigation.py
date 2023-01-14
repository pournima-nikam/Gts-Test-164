from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import html 
from selenium.webdriver.chrome.service import Service

def chromedriver():
    browser = webdriver.Chrome(service=Service('C:\\Translation EXE\\chromedriver.exe'))
    browser.get('https://vendor.myfloridamarketplace.com/search/bids')
    browser.maximize_window()
    time.sleep(2)
    navigation(browser)

def remove_html(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'',str(text))
    return cleantext
    
def navigation(browser):
    for max_result in browser.find_elements(By.XPATH,'//*[@class="mat-select-arrow ng-tns-c63-9"]'):
        max_result.click()
        time.sleep(3)
        break
    for clicking100 in browser.find_elements(By.XPATH,'//*[@id="mat-option-4"]/span'):
        clicking100.click()
        time.sleep(2)
        break
    for ad_status in browser.find_elements(By.XPATH,'//*[@id="mat-expansion-panel-header-1"]/span[2]'):
        ad_status.click()
        time.sleep(3)
        break
    for open in browser.find_elements(By.XPATH,'//*[@id="cdk-accordion-child-1"]/div/mat-selection-list/mat-list-option[2]/div/mat-pseudo-checkbox'):
        open.click()
        time.sleep(2)
        break 
    for search in browser.find_elements(By.XPATH,'//*[@type="submit"]/span[1]'):
        search.click()
        time.sleep(2)
        break  
    
    count = 1
    number_list = []
    a = True
    while a == True:
        for _ in browser.find_elements(By.XPATH,'//*[@class="mat-table cdk-table ng-star-inserted"]/tbody/tr/td[2]/a/span[1]'):
            temp_list = []
            for number in browser.find_elements(By.XPATH,'//*[@class="mat-table cdk-table ng-star-inserted"]/tbody/tr['+str(count)+']/td[2]/a/span[1]'):
                number_text = number.get_attribute('innerText').strip()
                link = 'https://vendor.myfloridamarketplace.com/search/bids/detail/'+ number_text.partition('-')[2]                  
                temp_list.append(link)
                print(link)    
                break
            for title in browser.find_elements(By.XPATH,'//*[@class="mat-table cdk-table ng-star-inserted"]/tbody/tr['+str(count)+']/td[1]'):
                title_text = title.get_attribute('innerText').strip()
                temp_list.append(title_text)
                print(title_text)
                break
            for purchaser in browser.find_elements(By.XPATH,'//*[@class="mat-table cdk-table ng-star-inserted"]/tbody/tr['+str(count)+']/td[5]'):
                purchaser_text = purchaser.get_attribute('innerText').strip()
                temp_list.append(purchaser_text)
                print(purchaser_text)
                break
            count += 1
            number_list.append(temp_list)
            
        for next_page in browser.find_elements(By.XPATH,'//*[@class="mat-paginator-range-actions"]/button[2]'):
            next_page_html = next_page.get_attribute('outerHTML')
            if  'disabled="true"' not in next_page_html:
                next_page.click()
                time.sleep(2)
                count = 1
                a = True
            else:
                a = False
    scrap(browser,number_list)            
        
def scrap(browser,number_list):
    for link in number_list:
        browser.get(link[0])
        time.sleep(2)
        
        segfileid = []   
            
        for _ in range(50):
            segfileid.append('')
        for data in browser.find_elements(By.XPATH,'//*[@class="scroll-content flex flex-vertical"]/div'):
            data_html = data.get_attribute('outerHTML')  
            break
        
        publish_date = data_html.partition('Published Date/Time:')[2].partition('</span>')[0]
        publish_date_text = remove_html(publish_date).strip()
        print(publish_date_text)
        
        start_date = data_html.partition('Start Date/Time:')[2].partition('</b>')[0]
        start_date_text = remove_html(start_date).strip()
        print(start_date_text)
        
        end_date = data_html.partition('End Date/Time:')[2].partition('</b>')[0]
        end_date_text = remove_html(end_date).replace('&nbsp;','').strip()
        segfileid[24] = end_date_text
        print(end_date_text)
        
        Agency_Number = data_html.partition('Agency Advertisement Number:')[2].partition('</div>')[0]
        Agency_Number_text = remove_html(Agency_Number).strip()
        print(Agency_Number_text)
        
        name = data_html.partition('Name:</span>')[2].partition('</span>')[0]
        name_text = remove_html(name).strip()
        print(name_text)
        
        phone = data_html.partition('Phone:</span>')[2].partition('</span>')[0]
        phone_text = remove_html(phone).strip()
        print(phone_text)
        
        address = data_html.partition('Address:</span>')[2].partition('</span>')[0]
        address_text = remove_html(address).strip()
        print(address_text)
        
        email = data_html.partition('Email:</span>')[2].partition('</a>')[0]
        email_text = remove_html(email).strip()
        print(email_text)
        
        segfileid[2] = ('Name: '+ name_text + '<br>\nPhone: ' + phone_text + '<br>\nAddress: ' + address_text + '<br>\nEmail: ' + email_text).title()
        
        segfileid[46] = ('Agency Advertisement Number: ' + Agency_Number_text + '<br>\nPublish_Date: ' + publish_date_text + '<br>\nStart_Date: ' + start_date_text)
        
        segfileid[19] = link[1]
        
        segfileid[12] = link[2]
        
        segfileid[31] = "vendor.myfloridamarketplace.com" 
        
        segfileid[7] = "MY"
        
        segfileid[28] = str(browser.current_url)
        
        segfileid[42] = segfileid[7] 
        
        for SegIndex, segfileid_data in enumerate(segfileid):
            print(SegIndex,segfileid_data)
        segfileid[SegIndex] = html.unescape((str(segfileid[SegIndex])))
        segfileid[SegIndex] = str(segfileid[SegIndex]).replace("'", "''")
        
        if segfileid[18] == '':
            segfileid[18] = segfileid[19]
            
        if len(segfileid[19]) >= 200:
            if segfileid[18] != segfileid[19]:
                segfileid[18] = segfileid[19]+'<br>\n'+segfileid[18]
            segfileid[19] = str(segfileid[19])[:200]+'...'
            
        if len(segfileid[46]) >= 1500:
                segfileid[46] = str(segfileid[46])[:1500]+'...'
    
chromedriver()
