#import pandas as pd
#import numpy as np
from selenium import webdriver
import json
import time


with open('tools/zzsecrets.json') as f:
    data = json.load(f)
    SECRET_RECOVERY_PHRASE = data['SECRET_RECOVERY_PHRASE']
    NEW_PASSWORD = data['NEW_PASSWORD']

with open('tools/conf.json') as f:
    data = json.load(f)
    MARKET_URL = data['marketUrl']
    NETWORK = data['network']
    NETWORK_URL = data['networkUrl']
    CHAINID = data['chainId']
    SYMBOL = data['symbol']
    BLOCK_EXPLORER = data['blockExplorer']

EXTENSION_PATH = 'tools/metamask_10.1.0_0.crx'
opt = webdriver.ChromeOptions()
opt.add_extension(EXTENSION_PATH)

driver = webdriver.Chrome('tools\chromedriver.exe',options=opt)

driver.switch_to_window(driver.window_handles[0])
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
time.sleep(2)

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
inputs[1].send_keys(NETWORK_URL)
inputs[2].send_keys(CHAINID)
inputs[3].send_keys(SYMBOL)
inputs[4].send_keys(BLOCK_EXPLORER)
driver.find_element_by_xpath('//button[text()="Save"]').click()

# Open marketplace
driver.get(MARKET_URL)

# Click "Login" on cryptobay page
driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div[2]/a').click()

# Select Metamask as a login
driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/span').click()
time.sleep(1)

# Get Metamask window
driver.switch_to_window(driver.window_handles[2])
driver.find_element_by_xpath('//button[text()="Next"]').click()
driver.find_element_by_xpath('//button[text()="Connect"]').click()

# Get cryptobay page 
driver.switch_to_window(driver.window_handles[0])
# Select "Marketplace" tab
driver.find_element_by_xpath('/html/body/div/div/header/div/div[1]/div/a[3]').click()

# Select "Dashboard" tab
driver.find_element_by_xpath('/html/body/div/div/header/div/div[1]/div/a[1]').click()
time.sleep(60)
#driver.quit()