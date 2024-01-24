import re
import time
import json
import socket
from sound.ring import ring
from datetime import datetime
from selenium import webdriver
from util.database_util import *
from config.news_info import NewsAddress
from config.ticker_name import Ticker_name
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.support import expected_conditions as EC


class NewsBot():

    def __init__(self,db_name,address,split_word):
        self.db_name = db_name
        self.address = address
        self.split_word = split_word
        self.kosdaq_idx = Ticker_name().KOSDAQ_NAME_TICKER
        self.kospi_idx = Ticker_name().KOSPI_NAME_TICKER
        
        self.start()
        
        
    
    def send_data(self,data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 12345))
            s.sendall(json.dumps(data).encode('utf-8'))
        

    
    def start(self):
        
        create_db(self.db_name)
        driver = webdriver.Chrome()
        driver.get(self.address)
        cnt = 0

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
                        current_time = datetime.now()
                        formatted_time = current_time.strftime(f"%H:%M:%S:%f")
                        insert_number(number_part,self.db_name)
                        
                        filename = 'news_time.txt'
                        with open(filename, 'w', encoding = 'utf-8') as file:
                            file.write(f"{title} - time : {formatted_time}")
                        print(formatted_time)
                        
                        # print(title)
                        # print(word)
                        # print(ticker)
                        # self.send_data(ticker)
                        ring()

                
                # id_to_delete = get_id_to_delete(self.db_name)  # Function to determine which ID to delete
                # if id_to_delete is not None:
                #     delete_id(self.db_name, id_to_delete)
                
                # print(title)
                time.sleep(1)
                
                if cnt % 3 == 0 : 
                    driver.refresh()
                elif cnt % 3 == 1 : 
                    driver.get(self.address)
                elif cnt % 3 == 2 : 
                    driver.execute_script("location.reload()")
                    cnt = 0 
                    
                cnt += 1

        except KeyboardInterrupt : 
            driver.quit()
        