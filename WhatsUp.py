from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests as req
import time

# phones = ["+79217714383", "+79954475361", "+79999836841", "+79814465925", "+79990886311"]

def connectwp(phones):
    driver = webdriver.Firefox()
    driver.get("https://web.whatsapp.com")
    # print("Scan QR Code, And then Enter")
    input("Scan QR Code, And then Enter")
    print("Logged In Whats`Up")
    # Set phone number
    print("start parse WhatsUp")
    for phon in phones:
        try:
            inp_xpath_search = "//div[@title='Текстовое поле поиска']"
            input_box_search = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
            input_box_search.click()
            #time.sleep(1)
            for x in range(12):
                input_box_search.send_keys(Keys.BACK_SPACE)
            input_box_search.send_keys(phon)
            # Click in chats
            #time.sleep(1)
            try:
                error = "//div[@class='f8jlpxt4 r5qsrrlp hp667wtd']//span"
                error = WebDriverWait(driver, 1).until(lambda driver: driver.find_element_by_xpath(error))
                if error.text == "Чаты, контакты и сообщения не найдены":
                    continue
            except: pass
            chats = "//div[@style='z-index: 0; transition: none 0s ease 0s; height: 72px; transform: translateY(72px);']"
            selected_contact = WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath(chats))
            selected_contact.click()
            # click person info
            #time.sleep(1)
            pers = "//div[@class='_2YnE3']"
            selected_contact = WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath(pers))
            selected_contact.click()
            # get Image
            #time.sleep(1)
            icon = "//div[@style='height: 200px; width: 200px; cursor: pointer;']//img[@class='_8hzr9 M0JmA i0jNr']"
            selected_contact = WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath(icon))
            url = selected_contact.get_attribute("src")
            resp = req.get(url)
            with open("images/WhastUp/"+phon+".jpg", "wb") as file:
                file.write(resp.content)
        except:
            pass
    driver.quit()