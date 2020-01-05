#with slight changes can also scrap journals name

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd

#options = Options()
#options.headless = True
delay = 3



file = open("journal.txt", "w")

#website = "https://dblp.uni-trier.de/db/conf/?pos="
website = "https://dblp.uni-trier.de/db/journals/?pos="
for i in range(0, 47):
    suffix = i*100 + 1
    driver = webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe')
    web = website + str(suffix)
    driver.get(web)

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'hide-body')))
        #print("Page is ready!")
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        body = soup.find(id = 'browse-journals-output')
        data = body.find(class_ = 'hide-body')        

        for a in data.find_all('a'):
            temp = a['href']
            tempList = temp.split("/")
            acronym = tempList[5]
            fullform = a.text
            file.write(acronym + " > " + fullform + '\n')

    except TimeoutException:
        print("Loading took too much time!")
    driver.close()


file.close()

#UnicodeEncodeError: 'charmap' codec can't encode character '\u0131' in position 24: character maps to <undefined>
#above error is coming in few instances.
#as of now, enteries giving this error were stored manually.