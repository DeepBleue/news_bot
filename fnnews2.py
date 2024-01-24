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




def ring():
    playsound('./sound/voice.mp3')

def fnnews_open():
    
    driver = webdriver.Chrome()

    address = f"https://www.fnnews.com/search?page=&search_type=&cont_type=&period_type=&searchDateS=&searchDateE=&search_txt=dschoi"

    driver.get(address)
    
    return driver 
    
    
    
    
if __name__ == '__main__':
    
    cnt = 1
    kosdaq_idx = Ticker_name().KOSDAQ_NAME_TICKER
    kospi_idx = Ticker_name().KOSPI_NAME_TICKER
    db_name = 'news_db/fnnews.db'
    create_db(db_name)

    driver = fnnews_open()

    try : 
        while True : 
            ticker = None
            
            
            wait = WebDriverWait(driver, 10) 
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tit_thumb')))
            title = elements[0].text



            if '[특징주]' in title :
                list_art = driver.find_elements(By.CLASS_NAME, 'list_art')
                a_tags = list_art[0].find_elements(By.TAG_NAME, 'a')
                href = a_tags[0].get_attribute('href')
                number_part = href.split('https://www.fnnews.com/news/')[1]
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
                    
                    filename = 'fnnews_time.txt'
                    current_time = datetime.now()
                    formatted_time = current_time.strftime(f"%H:%M:%S:%f")
                    with open(filename, 'a', encoding = 'utf-8') as file:
                        file.write(f"{title} - time : {formatted_time} \n")

                    print(title)
                    print(formatted_time)
                    ring()
                
            if cnt % 100 == 0 : 
                driver.quit()
                time.sleep(1)
                driver = fnnews_open()
                cnt = 1 
                print('hello')
                continue
            
            # id_to_delete = get_id_to_delete(db_name)  # Function to determine which ID to delete
            # if id_to_delete is not None:
            #     delete_id(db_name, id_to_delete)

                    
                
            driver.refresh()
            time.sleep(1.5)
            cnt += 1
            
            
    except KeyboardInterrupt : 
        driver.quit()