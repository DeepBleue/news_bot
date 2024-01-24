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
import os
from gtts import gTTS
import playsound

def speak(text):
    tts = gTTS(text=text, lang='ko')

    # Use an absolute path or a path you know you have permissions for
    home_dir = os.path.expanduser('~')
    filename = os.path.join(home_dir, 'voice.mp3')
    
    tts.save(filename)
    playsound.playsound(filename)



def ring():
    playsound('./sound/voice.mp3')


def moneyS_open():
    driver = webdriver.Chrome()

    address = f"https://www.moneys.co.kr/search?q=%EC%9D%B4%EC%A7%80%EC%9A%B4&qtype=writers"

    driver.get(address)
    
    return driver
    
if __name__ == '__main__':
    
    kosdaq_idx = Ticker_name().KOSDAQ_NAME_TICKER
    kospi_idx = Ticker_name().KOSPI_NAME_TICKER

    db_name = 'news_db/moneyS.db'
    create_db(db_name)
    
    cnt = 1
    
    driver = moneyS_open()
    

    try : 
        while True : 
            ticker = None
            
            elements = driver.find_elements(By.CLASS_NAME, 'atc-item')
            a_tags = elements[0].find_elements(By.TAG_NAME, 'a')
            # print(a_tags)
            # title = a_tags[0].find_elements(By.CLASS_NAME, 'title')[0].text
            wait = WebDriverWait(driver, 10)  # Adjust timeout as needed
            title_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'title')))

            if title_elements:
                title = title_elements[0].text
            else:
                print("No elements with class 'title' found after waiting")
            
            if '[특징주]' in title :
                href = a_tags[0].get_attribute('href')
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
                    
                    filename = 'moneyS_time.txt'
                    current_time = datetime.now()
                    formatted_time = current_time.strftime(f"%H:%M:%S:%f")
                    with open(filename, 'a', encoding = 'utf-8') as file:
                        file.write(f"{title} - time : {formatted_time} \n")

                    print(title)
                    print(formatted_time)
                    speak(title)
                    ring()
                
            if cnt % 100 == 0 : 
                driver.quit()
                time.sleep(1)
                driver = moneyS_open()
                cnt = 1
                print('hello')
                continue
                
                
            driver.refresh()
            time.sleep(1.5)
            
            id_to_delete = get_id_to_delete(db_name)  # Function to determine which ID to delete
            if id_to_delete is not None:
                delete_id(db_name, id_to_delete)
                    

            # driver.find_element(By.CSS_SELECTOR, "a[href='javascript:checkForm()").click()   
            # driver.find_element(By.XPATH, "//a[img[@alt='검색']]").click()
            
            
            
    except KeyboardInterrupt : 
        driver.quit()
        