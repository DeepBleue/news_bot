import re
import time
from selenium import webdriver
from playsound import playsound
from util.database_util import *
from selenium.webdriver.common.by import By
from config.ticker_name import Ticker_name
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from datetime import datetime



kosdaq_idx = Ticker_name().KOSDAQ_NAME_TICKER
kospi_idx = Ticker_name().KOSPI_NAME_TICKER

db_name = 'news_db/dnews.db'
create_db(db_name)


def ring():
    playsound('./sound/voice.mp3')
    
    

driver = webdriver.Chrome()

address = f"https://www.dnews.co.kr"

driver.get(address)

driver.switch_to.frame('startmain')

driver.execute_script("document.querySelector('.btn_search').click();")
driver.execute_script("document.getElementById('query').value = '54321';")
driver.execute_script("document.querySelector('.searching').click();")

try : 
    while True : 
        ticker = None
        
        # elements = driver.find_elements(By.CLASS_NAME, 'lineUse')
        wait = WebDriverWait(driver, 10) 
        elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lineUse')))
        a_tags = elements[0].find_elements(By.TAG_NAME, 'a')
        title = a_tags[0].find_elements(By.CLASS_NAME, 'title')[0].text

        
        if '[특징주]' in title :
            href = a_tags[0].get_attribute('href')
            number_part = href.split('idxno=')[1]
            pattern = r"\[특징주\]\s*(\w+)"
            match = re.search(pattern, title)
            word = match.group(1).strip()
            

            try : 
                ticker = kosdaq_idx[word]
            except : 
                pass  
            try : 
                ticker = kospi_idx[word]
            except : 
                pass
            if ticker == None : 
                print(f'there is no ticker {word}')

            elif (ticker != None) and (not number_exists(number_part,db_name)):
                insert_number(number_part,db_name)
                
                filename = 'dnews_time.txt'
                current_time = datetime.now()
                formatted_time = current_time.strftime(f"%H:%M:%S:%f")
                with open(filename, 'a', encoding = 'utf-8') as file:
                    file.write(f"{title} - time : {formatted_time} \n")

                print(title)
                print(formatted_time)
                ring()
        
            # print(href)
            # print(title)
            # print(word)
            # print(ticker)
        
        # id_to_delete = get_id_to_delete(db_name)  # Function to determine which ID to delete
        # if id_to_delete is not None:
        #     delete_id(db_name, id_to_delete)
                
            
        driver.find_element(By.CSS_SELECTOR, "a[href='javascript:checkForm()").click()   
        # driver.find_element(By.XPATH, "//a[img[@alt='검색']]").click()
        # print('refresh...')
        time.sleep(1.5)
        
        
        
        
        
        
        
        
        
        # for element in elements:
        #     a_tags = element.find_elements(By.TAG_NAME, 'a')
        #     for a_tag in a_tags:
        #         href = a_tag.get_attribute('href')
        #         title = a_tag.find_elements(By.CLASS_NAME, 'title')[0].text
                
        #         print(href)
        #         print(title)
                
                
        #         number_part = href.split('idxno=')[1]
        #         if not number_exists(number_part,db_name):
        #             insert_number(number_part,db_name)
        #             ring()
        

        

        
                    
except KeyboardInterrupt : 
    driver.quit()
    