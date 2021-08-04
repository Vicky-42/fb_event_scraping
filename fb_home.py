import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import os
import urllib.request
import pandas as pd
from datetime import datetime

#---------- XPath ------ one element ----------------
def elementFinder(element, action="", text=""):
    htmlElement = None
    waiting = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, element)))
    wait = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, element)))
    htmlElement = driver.find_element_by_xpath(element)
    if action == "click":
        driver.execute_script("arguments[0].click();", htmlElement)
    if action == "sendKeys":
        htmlElement.clear()
        htmlElement.send_keys(text)

def event_scraper():
    # login to facebook
    driver.get('https://www.facebook.com/')
    elementFinder('//input[@id="email"]','sendKeys','mikael@minhemstad.se')
    elementFinder('//input[@id="pass"]','sendKeys','Rappakalja12345')
    elementFinder('//button[@name="login"]','click')
    # accept the cookies pop up
    elementFinder('(//span[text()="Accept All"])[1]','click')
    # open events page and extract upcoming events
    page_links = pd.read_csv('event_sources.csv')
    df_csv = pd.DataFrame(columns=['Time','Name','ImageLink','Location','HostedBy','TicketLink','Info','Type','Co-ordinates','PageLink'])
    for i, row in page_links.iterrows():
        driver.get(row['Page links'])
        try:
            elementFinder('(//span[text()="Accept All"])[1]', 'click')
        except:
            pass
        # click on see more
        more_events = True
        while more_events == True:
            try:
                elementFinder('//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]/descendant::span[text()="See more"]','click')
            except:
                more_events = False
        # for each event in the page
        events = [event for event in driver.find_elements_by_xpath(
            '//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]/descendant::div[@class="j83agx80 cbu4d94t mysgfdmx hddg9phg"]')]
        for event_num in range(1,events.__len__()):
            event_row = []
            # click on the event link
            events = [event for event in driver.find_elements_by_xpath(
                '//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]/descendant::div[@class="j83agx80 cbu4d94t mysgfdmx hddg9phg"]')]
            try:
                events[event_num].find_element_by_xpath('./descendant::a').click()
            except:
                more_events = True
                while more_events == True:
                    try:
                        elementFinder(
                            '//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]/descendant::span[text()="See more"]',
                            'click')
                    except:
                        more_events = False
                try:
                    events = [event for event in driver.find_elements_by_xpath(
                        '//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]/descendant::div[@class="j83agx80 cbu4d94t mysgfdmx hddg9phg"]')]
                    events[event_num].find_element_by_xpath('./descendant::a').click()
                except:
                    break
            wait = WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH,
            '//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]')))
            # event time
            try:
                event_row.append(driver.find_element_by_xpath(
                    '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[1]').get_attribute('innerText'))
            except:
                try:
                    elementFinder('//span[text()="Reload Page"]','click')
                    elementFinder('//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[1]')
                    event_row.append(driver.find_element_by_xpath(
                        '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[1]').get_attribute('innerText'))
                except:
                    event_row.append('Event time does not exist')
            # event name
            try:
                event_row.append(driver.find_element_by_xpath(
                    '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[2]').get_attribute('innerText'))
                print('Event: {0}'.format(driver.find_element_by_xpath(
                    '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[2]').get_attribute('innerText')))
            except:
                event_row.append('Event name does not exist')
            # save event image
            try:
                # image_url = driver.find_element_by_xpath(
                #         '//div[@class="do00u71z l9j0dhe7 k4urcfbm ni8dbmo4 stjgntxs"]/descendant::img[@data-imgperflogname="profileCoverPhoto"]'
                #     ).get_attribute('src')
                # urllib.request.urlretrieve(image_url, os.path.join(
                #         os.path.abspath(os.getcwd()), 'Images {0}'.format(datetime.today().strftime('%Y-%m-%d')), '{0}.png'.format(image_num)))
                # event image link
                # event_row.append(os.path.join(os.path.abspath(os.getcwd()), 'Images {0}'.format(datetime.today().strftime('%Y-%m-%d')), '{0}.png'.format(image_num)))
                event_row.append(driver.find_element_by_xpath(
                        '//div[@class="do00u71z l9j0dhe7 k4urcfbm ni8dbmo4 stjgntxs"]/descendant::img[@data-imgperflogname="profileCoverPhoto"]'
                    ).get_attribute('src'))
            except:
                event_row.append('Event image does not exist')
            # event location
            try:
                event_row.append(driver.find_element_by_xpath(
                    '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[3]').get_attribute('innerText'))
            except:
                event_row.append('Event location does not exist')
            # event hosted by
            try:
                event_row.append(driver.find_element_by_xpath(
                    '//div[@class="sjgh65i0"]/descendant::span[contains(text(),"Event by ")]').get_attribute('innerText'))
            except:
                event_row.append('Event host name does not exist')
            # event ticket link
            try:
                event_row.append(driver.find_element_by_xpath(
                    '//div[@class="sjgh65i0"]/descendant::span[contains(text(),"Tickets")]/parent::div/following-sibling::div/span')
                    .get_attribute('innerText'))
            except:
                event_row.append('Event ticket link does not exist')
            # event info
            try:
                event_row.append(driver.find_element_by_xpath(
                    '(//div[@class="sjgh65i0"]/descendant::div[@class="dati1w0a hv4rvrfc"]/span)[1]')
                    .get_attribute('innerText'))
            except:
                event_row.append('Event info does not exist')
            # event type
            try:
                event_row.append(driver.find_element_by_xpath(
                    '//div[@class="sjgh65i0"]/descendant::div[@class="lhclo0ds j83agx80"]')
                    .get_attribute('innerText'))
            except:
                event_row.append('Event type does not exist')
            # event coordinates
            try:
                event_row.append(driver.find_element_by_xpath(
                    '//div[@class="sjgh65i0"]/descendant::div[@class="ihqw7lf3"]/descendant::span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh m9osqain hzawbc8m"]'
                ).get_attribute('innerText'))
            except:
                event_row.append('Event co-ordinates does not exist')
            # event page url
            event_row.append(driver.current_url)
            driver.back()
            elementFinder('//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]/descendant::div[@class="j83agx80 cbu4d94t mysgfdmx hddg9phg"]')
            df_csv.loc[len(df_csv)] = event_row
            df_csv.to_csv('Event Details {}.csv'.format(datetime.today().strftime('%Y-%m-%d')) ,index=False)

if __name__ == '__main__':
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    option = Options()
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    option.add_argument("--disable-infobars")
    option.add_argument('--disable-gpu')
    option.add_argument('--no-sandbox')
    option.binary_location = GOOGLE_CHROME_PATH
    # option.add_argument("--disable-extensions")
    driver = webdriver.Chrome(CHROMEDRIVER_PATH,chrome_options=option)
    print('Running Chromedriver....')
    # driver.maximize_window()
    event_scraper()
    print('Done')

