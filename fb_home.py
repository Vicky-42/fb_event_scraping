from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import sys, os,shutil, time
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
        events = [event for event in driver.find_elements_by_xpath('//div[@class="j83agx80 l9j0dhe7 k4urcfbm" and ./descendant::span[contains(text(),"Upcoming events")]]/descendant::div[@class="j83agx80 cbu4d94t mysgfdmx hddg9phg"]')]
        for event_num in range(1,events.__len__()):
            event_row = []
            # click on the event link
            events[event_num].find_element_by_xpath('./descendant::a').click()
            # event time
            event_row.append(driver.find_element_by_xpath(
                '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[1]').get_attribute('innerText'))
            # event name
            event_row.append(driver.find_element_by_xpath(
                '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[2]').get_attribute('innerText'))
            # event location
            event_row.append(driver.find_element_by_xpath(
                '//div[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div[3]').get_attribute('innerText'))
            # event hosted by
            event_row.append(driver.find_element_by_xpath(
                '//div[@class="sjgh65i0"]/descendant::span[contains(text(),"Event by ")]').get_attribute('innerText'))
            # event ticket link
            event_row.append(driver.find_element_by_xpath(
                '//div[@class="sjgh65i0"]/descendant::span[contains(text(),"Tickets")]/parent::div/following-sibling::div/span')
                .get_attribute('innerText'))
            # event info
            event_row.append(driver.find_element_by_xpath(
                '(//div[@class="sjgh65i0"]/descendant::div[@class="dati1w0a hv4rvrfc"]/span)[1]')
                .get_attribute('innerText'))
            # event type
            event_row.append(driver.find_element_by_xpath(
                '//div[@class="sjgh65i0"]/descendant::div[@class="lhclo0ds j83agx80"]')
                .get_attribute('innerText'))
            # event coordinates
            event_row.append(driver.find_element_by_xpath(
                '(//div[@class="sjgh65i0"]/descendant::div[@class="j83agx80 cbu4d94t ew0dbk1b irj2b8pg"]/descendant::span)[2]'
            ).get_attribute('innerText'))
            print('great success')

if __name__ == '__main__':
    chromedriver_path = os.path.join(os.path.abspath(os.getcwd()), "chromedriver.exe")
    option = Options()
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chromedriver_path,chrome_options=option)
    print('Running Chromedriver....')
    # driver.maximize_window()
    event_scraper()
    print('Done')

# def finviz():
#     elementFinder('//a[text()="Screener"]','click')
#     elementFinder('//table[@class="screener-view-table"]/descendant::a[text()="Custom"]','click')
#     try:
#         elementFinder('//a[@class="filter" and contains(text(),"Settings")]','click')
#     except:
#         pass
#     should_restart = True
#     while should_restart:
#         try:
#             waiting = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//td[@class="filters-border"]/descendant::tr')))
#             list_of_columns = driver.find_elements_by_xpath('//td[@class="filters-border"]/descendant::tr')
#             should_restart = False
#             for row in list_of_columns:
#                 columns = row.find_elements_by_xpath('./td')
#                 for column in columns:
#                     if column.find_element_by_xpath('./input[@type="checkbox"]').get_attribute('checked') != 'true':
#                         column.find_element_by_xpath('./input[@type="checkbox"]').click()
#                         should_restart = True
#                         break
#                 if should_restart == True:
#                     break
#         except:
#             try:
#                 elementFinder('//button[@class="modal-elite-ad_close"]','click')
#                 should_restart = True
#             except:
#                 should_restart = False
#
# def save_table():
#     df = pd.DataFrame()
#     elementFinder('//select[@id="signalSelect"]')
#     columns_tags = driver.find_elements_by_xpath('(//div[@id="screener-content"]/descendant::table)[4]/descendant::tr[1]/td')
#     columns = [col.get_attribute('innerText') for col in columns_tags]
#     columns.insert(1, 'URL')
#     columns.extend(['Signal'])
#     signals = pd.read_csv('signal.csv')
#     signals_list =  signals['Selected signals'].tolist()
#     signals_list = [x for x in signals_list if str(x) != 'nan']
#     for signal in signals_list:
#         elementFinder('//select[@id="signalSelect"]/option[text()="{}"]'.format(signal))
#         driver.find_element_by_xpath('//select[@id="signalSelect"]/option[text()="{}"]'.format(signal)).click()
#         elementFinder('//select[@id="signalSelect"]/option[text()="{}"]'.format(signal))
#         data = []
#         table = driver.find_element_by_xpath('(//div[@id="screener-content"]/descendant::table)[4]')
#         next_page = True
#         while next_page:
#             table = driver.find_element_by_xpath('(//div[@id="screener-content"]/descendant::table)[4]')
#             body = table.find_elements_by_xpath('./descendant::tr')
#             for row in body:
#                 cells = row.find_elements_by_xpath('./td')
#                 # dont add header row
#                 if cells[1].get_attribute('innerText') != 'Ticker':
#                     one_row = []
#                     one_row = [cell.get_attribute('innerText') for cell in cells]
#                     one_row.insert(1,cells[1].find_element_by_xpath('./a').get_attribute('href'))
#                     one_row.extend(['{}'.format(signal)])
#                     data.append(one_row)
#             try:
#                 elementFinder('//a[@class="screener_arrow"]','click')
#             except:
#                 next_page = False
#         current_signal = pd.DataFrame(data)
#         df = df.append(current_signal)
#         df.to_csv('finviz {}.csv'.format(datetime.today().strftime('%Y-%m-%d')), index=False)
#     df.columns = columns
#     df.to_csv('finviz {}.csv'.format(datetime.today().strftime('%Y-%m-%d')), index=False)
