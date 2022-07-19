from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import requests as req
from bs4 import BeautifulSoup
import time
import progressbar

def connectwp(phones):
    barсounter = 0
    driver = webdriver.Firefox()
    driver.get("https://web.whatsapp.com")
    # print("Scan QR Code, And then Enter")
    input("Scan QR Code, And then Enter")
    print("Logged In Whats`Up")
    # Set phone number
    print("start parse WhatsUp")
    lenght = len(phones)
    with progressbar.ProgressBar(max_value=lenght) as bar:
        for phon in phones:
            barсounter += 1
            bar.update(barсounter)
            try:
                inp_xpath_search = "//div[@title='Текстовое поле поиска']"
                input_box_search = WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
                input_box_search.click()
                #time.sleep(1)
                for x in range(13):
                    input_box_search.send_keys(Keys.BACK_SPACE)
                time.sleep(1)
                input_box_search.send_keys(phon)
                # Click in chats
                time.sleep(5)
                # get soup
                resp = driver.page_source
                soup = BeautifulSoup(resp, 'html.parser')
                try:
                    chats_b = soup.find('div', {'style': 'z-index: 0; transition: none 0s ease 0s; height: 72px; transform: translateY(72px);'}).find('img')
                    if chats_b != None:
                        chats = "//div[@style='z-index: 0; transition: none 0s ease 0s; height: 72px; transform: translateY(72px);']"
                        selected_contact = WebDriverWait(driver, 3).until(
                            lambda driver: driver.find_element_by_xpath(chats))
                        selected_contact.click()
                        time.sleep(1)
                        pers = "//div[@class='_2YnE3']"
                        selected_contact = WebDriverWait(driver, 10).until(
                            lambda driver: driver.find_element_by_xpath(pers))
                        selected_contact.click()
                        # get Image
                        time.sleep(1)
                        icon = "//div[@style='height: 200px; width: 200px; cursor: pointer;']//img[@class='_8hzr9 M0JmA i0jNr']"
                        selected_contact = WebDriverWait(driver, 10).until(
                            lambda driver: driver.find_element_by_xpath(icon))
                        url = selected_contact.get_attribute("src")
                        resp = req.get(url)
                        with open("images/WhastUp/" + phon + ".jpg", "wb") as file:
                            file.write(resp.content)
                    else:
                        with open("images/WhastUp/nopict.txt", "a") as file:
                            file.write(phon + "\n")
                        continue

                except:
                    pass
            except:
                with open("images/WhastUp/nopict.txt", "a") as file:
                    file.write(phon+"\n")
                pass
    driver.quit()