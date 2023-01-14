from cgitb import text
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
import html
import sys
import wx
App = wx.App()
import os 
import mysql.connector 



def CompanyInfoDB_connection():
    connection = ''
    a = 0
    while a == 0:
        try:
            connection = mysql.connector.connect(host='185.142.34.92',user='ams',passwd='TgdRKAGedt%h',database='companyinfo_db',charset='utf8')
            return connection
        except mysql.connector.ProgrammingError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                "\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def chromedriver(): # function

    browser = webdriver.Chrome('C:\\Translation EXE\\chromedriver.exe')  #chromedriver path
    browser.get('https://simap.org.pk/member-directory/')  #website
    browser.maximize_window()
    time.sleep(2)
    navigation(browser)   # function calling

def remove_html(text):
    clean = re.compile('<.*?>')
    cleantext = re.sub(clean,'',str(text))
    return cleantext

def navigation(browser):
    
    for submit in browser.find_elements(By.XPATH,'//*[@class="elementor-shortcode"]/form/div/ul/li[3]/input[2]'):
        submit.click()
        time.sleep(2)
        break
    a = 1 # link position (where is my link ?)
    # link_list = []
    # page_count = 1
    # count = 1
    # error = True
    # while error == True:
    #     for  _ in browser.find_elements(By.XPATH,'//*[@id="main"]/div/article/div/div/header/h2/a'):
    #         # pass
    #         for link in browser.find_elements(By.XPATH,'//*[@id="main"]/div/article['+str(count)+']/div/div/header/h2/a'):
    #             company_href = link.get_attribute('href')
    #             company_text = link.get_attribute('innerText')
    #             link_list.append(company_href+'****'+company_text) #conctenation(seperate two different things +'###'+)
    #             print(company_href,company_text)
    #         count += 1  # increament 1 by (append+=)

    #     for next_page in browser.find_elements(By.CLASS_NAME,"nav-links"):
    #         next_page_html = next_page.get_attribute('outerHTML')
    #     # if page_count != 2:
    #     if "Next Page" in next_page_html:
    #         for next in browser.find_elements(By.XPATH,'//*[@id="primary"]/div/nav/div/a'):   
    #             next_page_href = next.get_attribute('href')
    #             next_page_text = next.get_attribute('innerText')
    #             if 'Next Page →' in next_page_text:
    #                 next.click()
    #                 # browser.get(next_page_href)
    #                 time.sleep(3)
    #                 count = 1 #(1 to 10 counting for a single page)
    #                 error = True
    #                 # page_count += 1
    #     else:        
    #         error = Falseg
    #     # else:
    #     #     error = False

    # path = 'links'
    # file1 = open(path,"w")
    # file1.writelines(link_list) 
    # file1.close()
    # lines = ["Hello", "World"]

    # print("Total Link Collected:",len(link_list))
    
    # with open('links.txt', 'w') as file:
    #     file.writelines('\n'.join(link_list))     

    path = '/home/gts-anil/Desktop/pournima/sigma.or.pk/links.txt'
    file1 = open(path,"r")
    link = file1.read()
    all_link = link.splitlines() 

    for links in all_link:
        company_href = links.partition('****')[0].strip() # strip is used to remove whitespace
        company_name = links.partition('****')[2].strip()
        browser.get('https://simap.org.pk/dewal-surgical-co/')
        time.sleep(2)

        for data in browser.find_elements(By.XPATH,'//*[@id="main"]/article/div/div'):
            data_html = data.get_attribute('outerHTML')
            break
        data_html = re.sub("\s+"," ",data_html) # \s is a whitespace character
        data_html = html.unescape(data_html) # decoding the html

        if '<tr>' not in data_html:
        
            email = re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+)', data_html) 
            # print(Email)
            if email != 0:
                Email_list = []

                for h in email: 
                    if h not in Email_list: # non repetation of email 
                        Email_list.append(h)

                for Email in Email_list:
                    print ('company_link: '+str(a), company_href)
                    company_name = company_name.title()

                    if len(company_name) >= 200:
                        company_name = company_name[:200]+'...'
                    print('company text: ', company_name)
                    print ('Email: ',Email)

                    # regex = re.compile("\+?\d[\( -]?\d{3}[\) -]?\d{3}[ -]?\d{2}[ -]?\d{2}")
                    # numbers = re.findall(regex,data_html)
                    Tel =''
                    tel = re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]',data_html)
                    for Tele in tel:
                        Tel += Tele+','
                    Tel = Tel.rstrip(',')
                    print('Phone: ',Tel)
                    
                    # a = remove_html(data_html)
                    if '<br>' not in data_html:
                        Address = data_html.split('<p>')
                        # add = remove_html(address)
                        address = Address.pop(-1).replace('</p>','').replace('</div>','')
                        print('Address: ',address)
                    else:
                        Address = data_html.split('<br>')
                        # add = remove_html(address)
                        address = Address.pop(-1).replace('</p>','').replace('</div>','')
                        print('Address: ',address)    

                    if '<br>' not in data_html:
                        contact = data_html.split('<p>')
                        contact_name = contact[2].replace('</p>','').strip()
                        print('Contact name: ',contact_name)
                    else:
                        contact = data_html.split('<br>')
                        contact_name = contact[1].replace('</p>','').strip()
                        print('Contact name: ',contact_name)

                    website = '' 
                    if ".net" in data_html:
                        Website = data_html.partition('www.')[2].partition('.net')[0]
                        if Website != '': # WEBSITE IS BLANK
                            website = 'http://www.'+Website+'.net'
                            print('Website: ',website)
                    else:
                        Website = data_html.partition('www.')[2].partition('.com')[0]
                        if Website != '':
                            website = 'http://www.'+Website+'.com'
                            print('Website: ',website)
                        

                    country = 'Pakistan'
                    country = Get_country_code(country)

                    insert_details(company_href,company_name,Email,address,contact_name,Tel,country,website,)
                    print('\n========================================= \n')

            a += 1

    wx.MessageBox('All Process Are Done', 'sigma.or.pk', wx.OK | wx.ICON_INFORMATION)   
    print('All Process Are Done')
    browser.close()
    sys.exit()

def insert_details(company_href,company_name,Email,address,contact_name,Tel,country,website):
    Org_NAME = str(company_name)
    Address = str(address)
    city = ''
    state = ''
    country = str(country)
    contact_name = str(contact_name)
    telphone = str(Tel)
    fax = ''
    mobile_no = ''
    Emailid = str(Email)
    skype_id = ''
    website = str(website)
    product_services = ''
    cpv = ''
    source = 'sigma.or.pk'
    doc_path = str(company_href)
    status = ''
    user = '7'  # 7 userid of pournima
    CompanyInfoDB_Local = CompanyInfoDB_connection()
    a = True
    while a == True:
        try:
            error = True
            while error == True:
                try:
                    CompanyInfoDB_Local = CompanyInfoDB_connection()
                    CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                    error = False
                except:
                    print('Error on Connection')
                    CompanyInfoDB_cursorLocal.close()
                    CompanyInfoDB_Local.close()
                    time.sleep(10)
                    error = True
            Duplicate_Email = "Select A_id from CompanyInfoInternational where email_id = '" + str(Emailid) + "'"
            CompanyInfoDB_cursorLocal.execute(Duplicate_Email)
            results = CompanyInfoDB_cursorLocal.fetchall()
            if len(results) > 0:
                print(' Duplicate Hai Ye Insert Nhi Hoga !!!')
                a = False
            else:
                insert_data_local = "INSERT INTO CompanyInfoInternational(org_name,Address,city,state,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (
                    str(Org_NAME), str(Address), str(city), str(state), str(country),
                    str(contact_name), str(telphone), str(fax), str(mobile_no), str(Emailid),
                    str(skype_id), str(website), str(product_services), str(cpv), str(source),
                    str(doc_path), str(status), str(user))
                CompanyInfoDB_cursorLocal.execute(insert_data_local, values)
                CompanyInfoDB_Local.commit()
                print('\nCompanyInfoInternational Main Insert Ho Gya Hai !!!')
                insert_On_L2L_data = "INSERT INTO CompanyInfo_Final(org_name,Address,city,state,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                insert_On_L2L_values = (
                    str(Org_NAME), str(Address), str(city), str(state), str(country),
                    str(contact_name),
                    str(telphone), str(fax), str(mobile_no), str(Emailid), str(skype_id),
                    str(website),
                    str(product_services), str(cpv), str(source), str(doc_path), str(status), str(user))

                CompanyInfoDB_cursorLocal.execute(insert_On_L2L_data, insert_On_L2L_values)
                CompanyInfoDB_Local.commit()
                
                print('CompanyInfo_Final Main Insert Ho Gya Hai !!!\n')
                a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",fname,"\n", exc_tb.tb_lineno)
            a = True
            wx.MessageBox('Error', 'Info', wx.OK | wx.ICON_ERROR)
            time.sleep(10)

def Get_country_code(country):
    if country == 'USA':
        Country_code = 'US'
        return Country_code
    elif country == 'CONGO, DEM. REPUBLIC':
        Country_code = 'US'
        return Country_code
    elif country == 'COTE d IVOIRE':
        Country_code = 'CI'
        return Country_code
    elif country == 'FYR MACEDONIA':
        Country_code = 'MK'
        return Country_code
    elif country == 'KOREA (DEMOCRATIC PEOPLE S REPUBLIC OF)':
        Country_code = 'KP'
        return Country_code
    elif country == 'KOREA (REPUBLIC OF)':
        Country_code = 'KP'
        return Country_code
    elif country == 'PALESTINIAN TERRITORIES':
        Country_code = 'PS'
        return Country_code
    elif country == 'SLOVAK REPUBLIC':
        Country_code = 'SK'
        return Country_code
    elif country == 'STATELESS':
        Country_code = 'state'
        return Country_code
    elif country == 'UNITED STATES OF AMERICA':
        Country_code = 'US'
        return Country_code
    elif country == 'VIET NAM':
        Country_code = 'VN'
        return Country_code
    elif country == 'UNITED STATES':
        Country_code = 'US'
        return Country_code
    elif country == 'UNITED STATES MINOR OUTLYING ISLANDS':
        Country_code = 'UM'
        return Country_code
    elif 'QATAR' in country:
        Country_code = 'QA'
        return Country_code
    elif 'COLORADO' in country:
        Country_code = 'CO'
        return Country_code
    elif 'South Korea' in country:
        Country_code = 'KR'
        return Country_code
    elif 'U.k.' in country:
        Country_code = 'GB'
        return Country_code
    elif 'U.s.a.' in country:
        Country_code = 'US'
        return Country_code
    elif 'Turks & Caicos Islands' in country:
        Country_code = 'TC'
        return Country_code
    elif 'Trinidad & Tobago' in country:
        Country_code = 'TT'
        return Country_code
    elif 'St. Vincent & Grenadines' in country:
        Country_code = 'VC'
        return Country_code
    elif 'Virgin Islands, American' in country:
        Country_code = 'VI'
        return Country_code
    elif 'Virgin Islands, British' in country:
        Country_code = 'VG'
        return Country_code
    elif 'St. Pierre & Miquelon' in country:
        Country_code = 'PM'
        return Country_code
    elif 'Antigua & Barbuda' in country:
        Country_code = 'AG'
        return Country_code
    elif 'United Arab Emirates' in country:
        Country_code = 'AE'
        return Country_code
    elif 'UNITED KINGDOM' in country:
        Country_code = 'AE'
        return Country_code
    else:
        a = True
        while a == True:
            try:
                CompanyInfoDB_Local = CompanyInfoDB_connection()
                CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                # country_code = country.capitalize()
                Country_code = "SELECT `Code` FROM `dms_country_tbl` WHERE `Country` = '"+str(country)+"'"
                # print(Country_code)
                CompanyInfoDB_cursorLocal.execute(Country_code)
                results = CompanyInfoDB_cursorLocal.fetchone()
                try:
                    results = results[0]
                except:
                    pass
                # print('Country code mil gaya hai!!!!!')
                return results
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n",exc_tb.tb_lineno)
                time.sleep(5)
                a = True


chromedriver() # for function calling



