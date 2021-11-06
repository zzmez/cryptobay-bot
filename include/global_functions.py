import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import error
import json
import requests


def init_driver() -> webdriver.chrome.webdriver.WebDriver:
    with open('tools/zzsecrets.json') as f:
        data = json.load(f)
        SECRET_RECOVERY_PHRASE = data['SECRET_RECOVERY_PHRASE']
        NEW_PASSWORD = data['NEW_PASSWORD']

    with open('tools/conf.json') as f:
        data = json.load(f)
        global MARKET_URL
        MARKET_URL = data['marketUrl']
        NETWORK = data['network']
        NETWORK_URL = data['networkUrl']
        CHAINID = data['chainId']
        SYMBOL = data['symbol']
        BLOCK_EXPLORER = data['blockExplorer']

    EXTENSION_PATH = 'tools/metamask_10.1.0_0.crx'
    opt = webdriver.ChromeOptions()
    opt.add_extension(EXTENSION_PATH)

    driver = webdriver.Chrome('tools/chromedriver_win.exe',options=opt)

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)

    driver.find_element_by_xpath('//button[text()="Get Started"]').click()
    driver.find_element_by_xpath('//button[text()="Import wallet"]').click()
    driver.find_element_by_xpath('//button[text()="No Thanks"]').click()

    # After this you will need to enter you wallet details

    time.sleep(1)

    inputs = driver.find_elements_by_xpath('//input')
    inputs[0].send_keys(SECRET_RECOVERY_PHRASE)
    inputs[1].send_keys(NEW_PASSWORD)
    inputs[2].send_keys(NEW_PASSWORD)
    driver.find_element_by_css_selector('.first-time-flow__terms').click()
    driver.find_element_by_xpath('//button[text()="Import"]').click()
    time.sleep(3)

    driver.find_element_by_xpath('//button[text()="All Done"]').click()
    time.sleep(1)


    #Close the "What's new" page
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()

    # Click on networks
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()

    ## Add BSC network to metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/li[7]/span').click()
    inputs = driver.find_elements_by_xpath('//input')
    inputs[0].send_keys(NETWORK)
    time.sleep(0.2)
    inputs[1].send_keys(NETWORK_URL)
    time.sleep(0.2)
    inputs[2].send_keys(CHAINID)
    time.sleep(0.2)
    inputs[3].send_keys(SYMBOL)
    time.sleep(0.2)
    inputs[4].send_keys(BLOCK_EXPLORER)
    driver.find_element_by_xpath('//button[text()="Save"]').click()
    time.sleep(0.2)

    create_accounts(driver, 5)

    time.sleep(3)
    driver.get(MARKET_URL)
    time.sleep(2)

    login_with_metamask(driver)
    return driver


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
 
def login_with_metamask(driver: webdriver.chrome.webdriver.WebDriver) -> callable:
    # Click "Login" on cryptobay page
    element = driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div[2]/span')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.5)

    # Select Metamask as a login
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[2]/span').click()
    time.sleep(3)

    # Get Metamask window
    driver.switch_to.window(driver.window_handles[2])
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[1]/input').click()
    driver.find_element_by_xpath('//button[text()="Next"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//button[text()="Connect"]').click()
    time.sleep(0.5)

    # Get cryptobay page 
    driver.switch_to.window(driver.window_handles[0])


def wait_on_element(driver: webdriver.chrome.webdriver.WebDriver, element: str) -> callable:
    x = 0
    while x < 10:
        try:
            time.sleep(1)
            driver.find_element_by_xpath(f"{element}")
            break
        except:
            driver.refresh()
            time.sleep(5)
            x += 1
            pass

def go_to_page(driver: webdriver.chrome.webdriver.WebDriver, page_number: int) -> callable:
    wait_on_element("/html/body/div/div/div/div[2]/div[2]/ul/div/input")
    element = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input")
    
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input").clear()
    driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input").send_keys(page_number)
    time.sleep(0.5)
    driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input").send_keys(Keys.RETURN)
    time.sleep(1)


def check_authenticity(driver: webdriver.chrome.webdriver.WebDriver, link_auction: str) -> bool:
    is_authentic = True
    ship_id = link_auction.split(sep='/')[-2]
    ship_web_json = requests.get(f"https://api.cryptobay.top/bay/cryptobaygetobject?\
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