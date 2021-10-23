import time
from selenium import webdriver
from os import error
import requests

def get_bnb_price():
    return
    
def check_if_element_exists(driver: webdriver.chrome.webdriver.WebDriver, element: str) -> bool:
    zztry = False
    x = 0
    while (zztry is False and x < 3):
        try:
            #ship_id = driver.find_element_by_xpath("//div[@class='tit']").text.split('#')[1]
            driver.find_element_by_xpath(element)
            time.sleep(1)
            zztry = True
        except:
            x += 1
            driver.refresh()
            time.sleep(3)
            pass
    return zztry
 

def check_authenticity(driver: webdriver.chrome.webdriver.WebDriver, link_auction: str) -> bool:
    is_authentic = True
    ship_id = link_auction.split(sep='/')[-2]
    ship_web_json = requests.get(f"https://api.cryptobay.io/bay/cryptobaygetobject?\
        data=%7B%22token_type%22%3A1%2C%22token_id%22%3A{ship_id}%2C%22\
        with_powerpoints%22%3Atrue%2C%22with_level%22%3Atrue%7D").json()

    driver.get(link_auction)
    element_buy = "/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[2]"
    if check_if_element_exists(driver, element_buy) == False:
        raise error("Element does not exist")
    stats_from_json = ['raw_space','raw_speed','raw_skill','raw_defence','raw_attack','raw_morale']
    stats_from_driver = ['space', 'speed', 'skill', 'defence', 'attack', 'morale']
    zipped_elements = zip(stats_from_json, stats_from_driver)
    
    for el_json, el_driver in zipped_elements:
        driver_stat = driver.find_element_by_xpath(f"//div[@class='{el_driver}']").text.split('\n')[1]
        if ship_web_json['data'][el_json] != driver_stat:
            is_authentic = False

    return is_authentic

def switch_account(driver: webdriver.chrome.webdriver.WebDriver, account: int) -> callable:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
    time.sleep(2)
    popup_element ='//*[@id="popover-content"]/div/div/section/header/div/button'
    try:
        driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()    # close the popup
    except:
        pass
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[2]/div').click()         # click on account icon
    driver.find_element_by_xpath(f'//*[@id="app-content"]/div/div[4]/div[4]/div[3]/div[{account}]/div[3]/div[1]').click() # switch to desired account
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def create_accounts(driver: webdriver.chrome.webdriver.WebDriver, num_accounts: int = 5) -> callable:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()    # close the popup
    
    for _i in range(num_accounts - 1):
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[2]/div').click()             # click on account icon
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div[6]').click()
        time.sleep(1)                            # click on Create account
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[2]/div/button[2]').click()  # click on Create
        time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])