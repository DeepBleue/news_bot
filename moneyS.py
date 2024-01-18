import re
import time
from selenium import webdriver
from playsound import playsound
from util.database_util import *
from selenium.webdriver.common.by import By
from config.kosdaq_name import Kosdaq_name

kosdaq_ind = Kosdaq_name().KOSDAQ_NAME_TICKER

db_name = 'news_db/moneyS.db'
create_db(db_name)


def ring():
    playsound('./sound/voice.mp3')
    
    

driver = webdriver.Chrome()

address = f"https://search.naver.com/search.naver?where=news&query=%EC%9D%B4%EC%A7%80%EC%9A%B4&sm=tab_opt&sort=1&photo=0&field=2&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=4&news_office_checked=1417&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&is_sug_officeid=0&office_category=0&service_area=0"

driver.get(address)

# driver.switch_to.frame('startmain')

# driver.execute_script("document.querySelector('.btn_search').click();")
# driver.execute_script("document.getElementById('query').value = '특징주';")
# driver.execute_script("document.querySelector('.searching').click();")




try : 
    while True : 
        # elements = driver.find_elements(By.CLASS_NAME, 'list_news')
        
        sp_nws1 = driver.find_elements(By.ID, 'sp_nws2')[0]
        news_tit = sp_nws1.find_elements(By.CLASS_NAME, 'news_tit')[0]
        title = news_tit.get_attribute('title')
        if '[특징주]' in title :
            pattern = r"\[특징주\]\s*(\w+)"
            match = re.search(pattern, title)
            word = match.group(1).strip()
            
            ticker = kosdaq_ind[word]
            print(word)
            print(ticker)
            ring()
            
        print(title)
        # for element in elements:
        #     content_element = driver.find_elements(By.CLASS_NAME, 'news_contents')
        #     for content in content_element : 
        #         news_tit_class = driver.find_elements(By.CLASS_NAME, 'news_tit')
        #         for news_tit in news_tit_class:
        #             title = news_tit.get_attribute('title')
        #             print(title)

                    
            
            
            
            
            
            
                # a_tags = content.find_elements(By.TAG_NAME, 'a')
                # for a_tag in a_tags:
                #     href = a_tag.get_attribute('href')
                #     print(href)
                #     number_part = href.split('idxno=')[1]
                #     if not number_exists(number_part,db_name):
                #         insert_number(number_part,db_name)
                #         ring()

        # # id_to_delete = get_id_to_delete(db_name)  # Function to determine which ID to delete
        # # if id_to_delete is not None:
        # #     delete_id(db_name, id_to_delete)
        time.sleep(3)
        driver.refresh()

except KeyboardInterrupt : 
    driver.quit()