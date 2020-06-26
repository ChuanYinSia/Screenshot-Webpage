import time
import os
import re
import platform
import hashlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib3.exceptions import ProtocolError
from datetime import date
import sys


def screenshot(start_time):
    links = ['https://www.buzzfeed.com/food',
             'https://www.self.com/food', 'https://www.theguardian.com/food']
    if links:
        print(len(links), 'record ready')
        path = "./chromedriver_2.45/chromedriver_" + platform.system()
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--disable-gpu")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-notifications')

        with webdriver.Chrome(path, chrome_options=options) as driver:
            for link in links:
                desktop = {'output': str(link),
                           'width': 1366,
                           'height': 768}
                mobile = {'output': str(link),
                          'width': 414,
                          'height': 736}

                linkWithProtocol = str(link)

                x = str(desktop['output']).split(
                    '//')[-1].split('/')[0]
                clean = re.search(r"\bwww\.\w+", x)
                if clean is None:
                    x = x
                else:
                    x = x.replace('www.', '')
                hash_obj = hashlib.md5(x.encode())
                xy = hash_obj.hexdigest()
                dirName = 'img/' + \
                    xy[0] + '/' + xy[1] + '/' + xy[2]
                if not os.path.exists(dirName):
                    os.makedirs(dirName)

                try:
                    driver.set_page_load_timeout(20)

                    driver.set_window_size(
                        desktop['width'], desktop['height'])
                    driver.get(linkWithProtocol)
                    time.sleep(2)
                    driver.save_screenshot(
                        './' + dirName + '/' + x + '.png')

                    driver.set_window_size(
                        mobile['width'], mobile['height'])
                    driver.get(linkWithProtocol)
                    time.sleep(2)
                    driver.save_screenshot(
                        './' + dirName + '/m.' + x + '.png')

                except TimeoutException as e:
                    print(str(e))
                except ProtocolError as e:
                    print('[*] ', str(e), "Failed request.")
                except UnexpectedAlertPresentException as e:
                    print("[*] Found alert: closing")
                    try:
                        alert = browser.switch_to_alert()
                        alert.accept()
                    except:
                        print('[*] ', str(e), "Failed accept alert")
    else:
        print('Done')


if __name__ == "__main__":
    start_time = time.time()
    try:
        screenshot(start_time)
    except Exception as e:
        print(e)

    print("--- %s seconds ---" % round(time.time() - start_time, 2))
