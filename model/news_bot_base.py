import re
import time
from selenium import webdriver
from util.database_util import *
from selenium.webdriver.common.by import By
from config.ticker_name import Ticker_name
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from config.news_info import NewsAddress
from sound.ring import ring

class NewsBot():

    def __init__(self,db_name,address,split_word):
        self.db_name = db_name
        self.address = address
        self.split_word = split_word
        self.kosdaq_idx = Ticker_name().KOSDAQ_NAME_TICKER
        self.kospi_idx = Ticker_name().KOSPI_NAME_TICKER
        
        self.start()
        
        
        
        
    
    
    def start(self):
        
        create_db(self.db_name)
        driver = webdriver.Chrome()
        driver.get(self.address)

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
                    number_part = href.split(self.split_word)[1]
                    pattern = r"\[특징주\]\s*(\w+)"
                    match = re.search(pattern, title)
                    word = match.group(1).strip()
                    try : 
                        ticker = self.kosdaq_idx[word]
                    except : 
                        pass  
                    try : 
                        ticker = self.kospi_idx[word]
                    except : 
                        pass
                    if ticker == None : 
                        print(f'there is no ticker {word}')

                    elif (ticker != None) and (not number_exists(number_part,self.db_name)):
                        insert_number(number_part,self.db_name)
                        print(word)
                        print(ticker)
                        ring()

                
                # id_to_delete = get_id_to_delete(self.db_name)  # Function to determine which ID to delete
                # if id_to_delete is not None:
                #     delete_id(self.db_name, id_to_delete)
                
                print(title)
                time.sleep(1)
                driver.refresh()
                

        except KeyboardInterrupt : 
            driver.quit()
        