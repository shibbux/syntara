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
options.add_argument('--disable-gpu')  # Disable GPU to avoid errors
options.add_argument('--no-sandbox')  # Disable sandbox mode if needed

def listen():
    driver = webdriver.Chrome(service=service, options=options)
    org = sys.stdout
    sys.stdout = silent()  # Suppress output to terminal from Selenium

    try:
        # Navigate to the page
        driver.get('https://aquamarine-llama-e17401.netlify.app/')
        print("Navigating to the page...")  # Debugging line to confirm page is loading

        # Try to find the textbox
        try:
            txt_box = driver.find_element(By.ID, "textbox")
            print("Textbox found!")  # Debugging line
        except Exception as e:
            print(f"Error finding the textbox: {e}")
            return

        last_txt = ""
        start_time = time.time()  # Start time to stop after 5 seconds

        while True:
            current_txt = txt_box.get_attribute('value')  # Get the text value from the textbox
            print(f"Current text: {current_txt}")  # Debugging line to see the text

            # Only write to the file if the text has changed
            if current_txt != last_txt:
                try:
                    with open('DATA\\input.txt', 'w') as file:
                        file.write(current_txt)
                        file.flush()
                        last_txt = current_txt
                    print(f"Writing to file: {current_txt}")  # Debugging message to confirm write
                except Exception as e:
                    print(f"Error writing to file: {e}")  # Debugging file write error

            # Stop after 5 seconds
            elapsed_time = time.time() - start_time
            if elapsed_time > 5:
                print("5 seconds passed, stopping input collection.")  # Debugging message
                break  # Exit loop after 5 seconds

            time.sleep(0.1)  # Small delay to prevent tight looping

        # After 5 seconds, print the contents of input.txt to the terminal
        

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
        sys.stdout = org  # Restore the original stdout to terminal


def read():

    try:
        if os.path.exists('DATA\\input.txt'):
            with open('DATA\\input.txt', 'r') as file:
                content = file.read()
                # print("\nContents of input.txt after 5 seconds:\n")
                print(content)  # Print the content of the file to terminal
        else:
            print("Error: input.txt does not exist!")  # Handle case where file is missing
    except Exception as e:
        print(f"Error reading input.txt: {e}")  # Catch and print error if reading fails

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


listen()

read()
