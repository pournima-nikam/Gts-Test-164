from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from datetime import datetime




def chromedriver():
    browser = webdriver.Chrome('/home/gts-anil/anil exe/Translation Exe/chromedriver') #chromedriver path
    browser.get('https://nsdctg.navy.mil.bd/tenders') #website
    browser.maximize_window()
    time.sleep(2)
    navigation(browser)
    

count = 1
def navigation(browser):
    global count
    tender_list = []
    div_count = 6 # value of div on 1st page
    next_div_count = 7 # value of div count on 1st page
    error = True
    while error == True:
        for _ in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr'):
            for tender_no in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr['+str(count)+']/td[3]'):
                tender_no_text = tender_no.get_attribute('innerText').strip()
                print(tender_no_text)
                break

            for tender_date in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr['+str(count)+']/td[4]'):
                tender_date_text = tender_date.get_attribute('innerText').strip()
                print(tender_date_text)
                break

            for category in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr['+str(count)+']/td[2]'):
                category_text = category.get_attribute('innerText').strip()
                print(category_text)
                break

            for tender_description in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr['+str(count)+']/td[5]'):
                tender_description_text = tender_description.get_attribute('innerText').strip()
                print(tender_description_text)
                break

            for opening_date in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr['+str(count)+']/td[7]'):
                opening_date_text = opening_date.get_attribute('innerText').strip()
                print(opening_date_text)
                break

            for notice in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr['+str(count)+']/td[9]/a'):
                notice_href = notice.get_attribute('href').strip()
                print(notice_href)
                break

            for specification in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(div_count)+']/div/table/tbody/tr['+str(count)+']/td[10]/a'):
                specification_href = specification.get_attribute('href').strip()
                print(specification_href)
                break


            tender_list.append({'Category:': category_text, 'Tender_No:':tender_no_text, 'Tender_Date:':tender_date_text, 'Tender_Description:': tender_description_text, 'Opening_Date:': opening_date_text, 'Notice:': notice_href, 'Specification:': specification_href})

            count += 1



        for next in browser.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/main/div/div/div/div['+str(next_div_count)+']/div/div[2]/nav/ul/li[4]/a/span/i'):
            next_text = next.get_attribute('outerHTML').strip()
            if "fa fa-caret-right fa-lg" in next_text: # (class = fa fa-caret-right fa-lg) common in all link in next
                next.click()
                time.sleep(2)
                div_count = 4 # value of div count changed from page 2
                next_div_count = 5 # value of next div count changed from page 2
                count = 1 # 1 to 20 counting on page
                error = True
            else: # next for loop break
                error = False  
    scrap(tender_list)

def scrap(tender_list):

    for data in tender_list:
        try:
            segfield = []
            for _ in range(50):
                segfield.append('')

            segfield[13] = data['Tender_No:']

            segfield[19] = data['Tender_Description:']

            t = data['Opening_Date:']
            w = datetime.strptime(t,'%d %b %Y') #strptime used for website date format declaration
            final_date = w.strftime('%Y-%m-%d') # strftime used for our format declaration
            segfield[24] = final_date

            segfield[46] = data['Category:']+"<br>\n"+data['Tender_Date:']

            segfield[5] = data['Notice:']

            segfield[6] = data['Specification:']

            check_date(segfield)
                
        except Exception as e:
            print(e)
            

def check_date(segfield):
    
    deadline = (segfield[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                check_Duplication(segfield)
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            Global_var.deadline_Not_given += 1
    except Exception as e:
        print(e)


        
        


    


        


                
        
    

    

chromedriver()