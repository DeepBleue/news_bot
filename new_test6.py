from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import discord
import asyncio
import nest_asyncio
from database_util import *
import winsound
from playsound import playsound

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



db_name = 'dnews.db'
create_db(db_name)


def ring():
    # winsound.Beep(1000, 100)
    playsound('./sound/voice.mp3')
    
    

driver = webdriver.Chrome()


driver.get(f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%B0%95%EC%97%B0%EC%98%A4&sort=1&photo=0&field=2&pd=0&ds=&de=&mynews=1&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:all,a:all&start=1")

# driver.switch_to.frame('startmain')

# driver.execute_script("document.querySelector('.btn_search').click();")
# driver.execute_script("document.getElementById('query').value = '특징주';")
# driver.execute_script("document.querySelector('.searching').click();")




try : 
    while True : 
        elements = driver.find_elements(By.CLASS_NAME, 'list_news')
        
        # print(elements)
        for element in elements:
            content_element = driver.find_elements(By.CLASS_NAME, 'news_contents')
            for content in content_element : 
            
                a_tags = content.find_elements(By.TAG_NAME, 'a')
                for a_tag in a_tags:
                    href = a_tag.get_attribute('href')
                    print(href)
                    number_part = href.split('idxno=')[1]
                    if not number_exists(number_part,db_name):
                        insert_number(number_part,db_name)
                        ring()

        # id_to_delete = get_id_to_delete(db_name)  # Function to determine which ID to delete
        # if id_to_delete is not None:
        #     delete_id(db_name, id_to_delete)
        time.sleep(1)
        driver.refresh()

except KeyboardInterrupt : 
    driver.quit()