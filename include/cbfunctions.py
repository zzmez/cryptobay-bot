from os import error
from selenium import webdriver
import time
import pandas as pd
from global_functions import check_authenticity, check_if_element_exists, switch_account

def buy_boat(driver: webdriver.chrome.webdriver.WebDriver, df: pd.DataFrame, account: int) -> callable:
    switch_account(driver, account)
    ship_id = str(df['ship_id'].values[0])
    transaction_id = str(df['transaction_id'].values[0])
    link_auction = f"https://marketplace.cryptobay.io/ship/{ship_id}/{transaction_id}"
    if check_authenticity(driver, link_auction) == True:
        driver.get(link_auction)
        element_buy = "/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[2]"
        if check_if_element_exists(driver, element_buy) == False:
            raise error("Element does not exist")
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(element_buy))
        driver.switch_to.window(driver.window_handles[1])       # switch to metamask window
        confirmation = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/div[3]/footer/button[2]') # Confirm
        # confirmation = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/div[3]/footer/button[1]') # Cancel - testing purposes
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(confirmation))
        driver.switch_to.window(driver.window_handles[0])       # switch back to marketplace window
        print(f"Bought ship {df['ship_id']} at the price of {df['predicted_price_BNB']}")
    else:
        print("Could not buy ship ")

def sell_boat(driver: webdriver.chrome.webdriver.WebDriver, price: float, account: int) -> callable:
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

    