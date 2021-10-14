import json
from selenium import webdriver
import time
import requests
import pandas as pd

def get_ship_stats_selling(bnb_price: float, raw_json: json):
    ship_id_list = pd.DataFrame([element['token_id'] for element in raw_json['data']['auctions']])
    tranzaction_id_list = pd.DataFrame([element['idx'] for element in raw_json['data']['auctions']])
    ship_class_list = pd.DataFrame([element['class'] for element in raw_json['data']['auctions']])
    ship_price_list_BNB = pd.DataFrame([ round(int(element['buyout_price']) / 1000000000, 3) for element in raw_json['data']['auctions'] ])
    ship_price_list_USD = pd.DataFrame([ round(int(element['buyout_price']) / 1000000000 * bnb_price, 2) for element in raw_json['data']['auctions'] ])

    boat_space_list = pd.DataFrame([ element['raw_space'] for element in raw_json['data']['auctions']])
    boat_speed_list = pd.DataFrame([ element['raw_speed'] for element in raw_json['data']['auctions']])
    boat_skill_list = pd.DataFrame([ element['raw_skill'] for element in raw_json['data']['auctions']])
    boat_defence_list = pd.DataFrame([ element['raw_defence'] for element in raw_json['data']['auctions']])
    boat_attack_list = pd.DataFrame([ element['raw_attack'] for element in raw_json['data']['auctions']])
    boat_morale_list = pd.DataFrame([ element['raw_morale'] for element in raw_json['data']['auctions']])
    
    concat_DF = pd.concat([ship_id_list, tranzaction_id_list, ship_class_list, \
                        boat_space_list, boat_speed_list, boat_skill_list, \
                        boat_defence_list, boat_attack_list, boat_morale_list,\
                        ship_price_list_USD, ship_price_list_BNB], axis=1)
    
    concat_DF.columns
    return concat_DF

def check_stats(driver: webdriver.chrome.webdriver.WebDriver, link_boat: str, link_auction: str):
    boat_id = 0
    r = requests.get(f"https://api.cryptobay.io/bay/cryptobaygetobject?\
        data=%7B%22token_type%22%3A1%2C%22token_id%22%3A{boat_id}%2C%22\
        with_powerpoints%22%3Atrue%2C%22with_level%22%3Atrue%7D").json()
    
    _link_boat_json = ""
    return


def buy_boat(driver: webdriver.chrome.webdriver.WebDriver, link_auction: str):
    return

def sell_boat(driver: webdriver.chrome.webdriver.WebDriver, account: int , price: float) -> callable:
    driver.get("https://marketplace.cryptobay.io/profile/inventory")  # click on my account
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[3]/div').click()   #click on the boat
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[1]').click()   #click on sell
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[3]/div[2]/input').clear()
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[3]/div[2]/input').send_keys(str(price))
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[4]/div').click()     #click on Confirm button
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[2])       # switch to metamask window
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]').click() # press Confirm
    driver.switch_to.window(driver.window_handles[0])
    ##LOGGING part    




def cancel_auction(driver: webdriver.chrome.webdriver.WebDriver, account: int = 0) -> callable:
    driver.get("https://marketplace.cryptobay.io/profile/inventory")  # click on my account
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span').click()   #click for dropdown menu
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/ul[2]/li[1]').click()   #select for sale
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[3]/div').click()    #select ship
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[3]').click()    #select cancel
    time.sleep(3)
    
    driver.switch_to.window(driver.window_handles[2])       # switch to metamask window
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]').click() # press Confirm
    driver.switch_to.window(driver.window_handles[0])
    ##LOGGING part

    