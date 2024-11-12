import os 
import time
import sys
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class silent:
    def write(self, msg):
        pass
    def flush(self):
        pass

driver_path = 'DATA\\Driver\\chromedriver.exe'

service = Service(driver_path)

options = Options()
options.add_argument('--use-fake-ui-for-media-stream')
options.add_argument('--headless')

def listen():
    driver = webdriver.Chrome(service=service,options=options)
    org = sys.stdout
    sys.stdout = silent()
    try:
        driver.get('https://aquamarine-llama-e17401.netlify.app/')
        txt_box = driver.find_element(By.ID,"textbox")
        last_txt = ""
        while True:
            current_txt = txt_box.get_attribute('value')
            if current_txt != last_txt:
                with open('DATA\\input.txt', 'w') as file:
                    file.write(current_txt)
                    file.flush()
                    last_txt = current_txt
                time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
        sys.stdout = org

listen()