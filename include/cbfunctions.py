from datetime import datetime, timezone, date
from os import error
import time
from IPython.terminal.shortcuts import reset_buffer
import pandas as pd
from selenium import webdriver

from include.global_functions import check_authenticity, check_if_element_exists, switch_account
from include.remote_calls import compute_price


def log_transaction(acc_id: int, tr_type: str, ship_id: int, \
                    tr_id: int, price: float, resale_discount: float = None,\
                    date: date = date.today().strftime('%Y-%m-%d')):
    tr_df = pd.read_csv("db/transactions/transactions_hist.csv")
    _columns = tr_df.columns
    _list = [date, acc_id, tr_type, ship_id, tr_id, price, resale_discount]
    _temp_row = pd.DataFrame([_list], columns=_columns)
    final_df = tr_df.append(_temp_row)
    final_df.to_csv("db/transactions/transactions_hist.csv", index=False)

def buy_boat(driver: webdriver.chrome.webdriver.WebDriver, df: pd.DataFrame, account: int) -> callable:
    switch_account(driver, account)
    ship_id = str(df['ship_id'].values[0])
    price = float(df['selling_price_BNB'].values[0])
    transaction_id = str(df['transaction_id'].values[0])
    link_auction = f"https://marketplace.cryptobay.top/ship/{ship_id}/{transaction_id}"
    if check_authenticity(driver, link_auction) == True:
        driver.get(link_auction)
        element_buy = "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]"
        if check_if_element_exists(driver, element_buy) == False:
            raise error("Element does not exist")
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(element_buy))
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])       # switch to metamask window
        confirmation = '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]' # Confirm
        # confirmation = '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[1]' # Cancel
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(confirmation))
        driver.switch_to.window(driver.window_handles[0])       # switch back to marketplace window
        log_transaction(account, "buy", ship_id, transaction_id, price)
    else:
        print("Could not buy ship ")

def sell_boat(driver: webdriver.chrome.webdriver.WebDriver, acc_id: int, resale_discount: float, price: float = None) -> callable:
    """
    Usage:  sell_boat(driver, 5, 0.85)  
        this automatically sets the price to 85% of the PREDICTED price !!! Not the actual price !!!
        or
            sell_boat(driver, 5, 1.0, 0.10) #this disregards the resale discount 
    """
    switch_account(driver, acc_id)

    driver.get("https://marketplace.cryptobay.top/profile/inventory")  
    time.sleep(3)
    check_if_element_exists(driver, '/html/body/div[1]/div/div/div/div[3]/div')
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div').click() #click the boat
    time.sleep(3)
    ship_str = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div[3]').text
    ship_id = int(ship_str.split("#")[1])
    ship_obj = compute_price(ship_id, resale_discount)

    if price is None:
        price = ship_obj.discounted_price()

    driver.find_element_by_xpath\
        ('/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]').click()   #click on sell
    driver.find_element_by_xpath\
        ('/html/body/div[4]/div[2]/div/div/div/div/div[3]/div[2]/input').clear()
    driver.find_element_by_xpath\
        ('/html/body/div[4]/div[2]/div/div/div/div/div[3]/div[2]/input').send_keys(str(price))
    driver.find_element_by_xpath\
        ('/html/body/div[4]/div[2]/div/div/div/div/div[4]/div').click()     #click on Confirm button
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[-1])       # switch to metamask window
    driver.find_element_by_xpath\
        ('//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]').click() # Confirm
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

    url = driver.current_url
    tr_id = int(url.split('/')[-1])

    log_transaction(acc_id, "resell", ship_id, tr_id, price, resale_discount)
    time.sleep(20)



def cancel_auction(driver: webdriver.chrome.webdriver.WebDriver, account: int = 0) -> callable:
    driver.get("https://marketplace.cryptobay.top/profile/inventory")  # click on my account
    time.sleep(6)
    switch_account(driver, account)
    time.sleep(6)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/span').click()   #click for dropdown menu
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/ul[2]/li[1]').click()   #select for sale
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div').click()    #select ship
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]').click()    #select cancel
    time.sleep(5)
    
    driver.switch_to.window(driver.window_handles[-1])       # switch to metamask window
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]').click() # press Confirm
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(20)

def resell_auction(driver: webdriver.chrome.webdriver.WebDriver, acc_id: int, resale_discount: float, price: float = None) -> callable:
    cancel_auction(driver, account=acc_id)
    sell_boat(driver, acc_id,resale_discount, price)

def resell_auction_pct(driver: webdriver.chrome.webdriver.WebDriver, acc_id: int, pct_resale: float = 10) -> callable:
    cancel_auction(driver, account=acc_id)
    time.sleep(15)
    trx_df = pd.read_csv("db/transactions/transactions_hist.csv")
    acc_df = pd.read_csv("db/accounts/account_status.csv")
    if acc_df.loc[acc_df['acc_id'] == acc_id, 'available'].bool() == False:
        new_price = float(trx_df[(trx_df['acc_id'] == acc_id) &
                         (trx_df['tr_type'] == 'resell')]['price'].tail(1))
        new_price = round(new_price * (100 - pct_resale)/100,3)
        sell_boat(driver, acc_id, resale_discount=1, price=new_price)
        