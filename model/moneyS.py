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


kosdaq_idx = Ticker_name().KOSDAQ_NAME_TICKER
kospi_idx = Ticker_name().KOSPI_NAME_TICKER

db_name = 'news_db/moneyS.db'
create_db(db_name)


def ring():
    playsound('./sound/voice.mp3')
    
    

driver = webdriver.Chrome()

address = f"https://search.naver.com/search.naver?where=news&query=%EC%9D%B4%EC%A7%80%EC%9A%B4&sm=tab_opt&sort=1&photo=0&field=2&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=4&news_office_checked=1417&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&is_sug_officeid=0&office_category=0&service_area=0"

driver.get(address)


try : 
    while True : 
        ticker = None
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "sp_nws1"))
            )
            sp_nws1 = element
        except TimeoutException:
            print("Timed out waiting for the element to load")        
        # sp_nws1 = driver.find_elements(By.ID, 'sp_nws1')[0]
        news_tit = sp_nws1.find_elements(By.CLASS_NAME, 'news_tit')[0]
        title = news_tit.get_attribute('title')

        if '[특징주]' in title :
            href = news_tit.get_attribute('href')
            number_part = href.split('https://www.moneys.co.kr/article/')[1]
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
                print(word)
                print(ticker)
                ring()
        
        # id_to_delete = get_id_to_delete(db_name)  # Function to determine which ID to delete
        # if id_to_delete is not None:
        #     delete_id(db_name, id_to_delete)
        
        
        print(title)
        time.sleep(1)
        driver.refresh()



except KeyboardInterrupt : 
    driver.quit()