import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time

# FUNCTIONS

def login_with_metamask():
    # Click "Login" on cryptobay page
    driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div[2]/a').click()
    time.sleep(0.5)

    # Select Metamask as a login
    driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/span').click()
    time.sleep(3)


def wait_on_element(element: str):
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


def go_to_page(page_number: int):
    wait_on_element("/html/body/div/div/div/div[2]/div[2]/ul/div/input")
    element = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input")
    
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input").clear()
    driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input").send_keys(page_number)
    time.sleep(0.5)
    driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/ul/div/input").send_keys(Keys.RETURN)
    time.sleep(1)

def get_initial_sold_from_marketplace(sold_already_exported: bool):
    if(sold_already_exported):
        return
    #driver.maximize_window()
    # Select "Dashboard" tab
    driver.find_element_by_xpath('/html/body/div/div/header/div/div[1]/div/a[1]').click()
    time.sleep(3)
    wait_on_element("/html/body/div/div/div/div[2]/div[2]/ul/div")
    raw_no_of_pages = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/ul/div').text
    no_of_pages = int(raw_no_of_pages.strip('/ '))
    
    with open(filename, mode='a+', buffering=1) as s:
    # Iterate backwards to the first page
        resume_page = no_of_pages - int(num_lines/10)

        for i in range(resume_page, 0, -1):
            go_to_page(i)

            no_of_elements = len(driver.find_elements_by_xpath("//div[@class='list-c'][2]//div[@class='item']"))
            for j in range(no_of_elements,0,-1):
                sold_price = driver.find_element_by_xpath(f"/html/body/div/div/div/div[2]/div[2]/div[2]/div[2]/div[{j}]/div[4]/span[1]").text.strip("Ξ ")
                # driver.find_element_by_xpath(f"//div[@class='list-c'][2]//div[@class='item'][{j}]").click()
                for attempt in range(5):
                    try:
                        # driver.find_element_by_xpath(f"/html/body/div/div/div/div[2]/div[2]/div[2]/div[2]/div[{j}]").click()
                        element = driver.find_element_by_xpath(f"/html/body/div/div/div/div[2]/div[2]/div[2]/div[2]/div[{j}]")
                        driver.execute_script("arguments[0].click();", element)
                        break
                    except:
                        print("Element ITEM not found (boat)")
                        time.sleep(2)
                        continue


                time.sleep(1)
                stats = get_ship_stats(sold_price)
                s.write(stats + "\n")
                driver.back()
                time.sleep(2)
                go_to_page(i)



def cancel_auction(driver: webdriver.chrome.webdriver.WebDriver, account: int = 0) -> callable:
    driver.get("https://marketplace.cryptobay.io/profile/inventory")  # click on my account
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span').click()   #click for dropdown menu
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/ul[2]/li[1]').click()   #select for sale
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[3]/div').click()    #select ship
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[3]/div').click()    #select cancel
    
    
    driver.switch_to.window(driver.window_handles[1])       # switch to metamask window
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/div[3]/footer/button[2]').click() # press Confirm
    driver.switch_to.window(driver.window_handles[0])

def get_ship_stats(ship_sold_price:int):
    transaction_id = driver.current_url.split('/')[-1]
    time.sleep(2)

    # A gimmyck to retry until it finds the element
    zztry = None
    while zztry is None:
        try:
            ship_id = driver.find_element_by_xpath("//div[@class='tit']").text.split('#')[1]
            time.sleep(1)
            zztry = True
        except:
            driver.refresh()
            time.sleep(5)
            pass
 
    # for attempt in range(5):
    #     try:
    #         # driver.find_element_by_xpath(f"/html/body/div/div/divd/div[2]/div[2]/div[2]/div[2]/div[{j}]").click()
    #         # there's a bug where it delogs you. you have to relog or refresh)
    #         if (driver.find_element_by_xpath("/html/body/div/div/header/div/div[2]/a")):
    #             time.sleep(1)
    #             ship_id = driver.find_element_by_xpath("//div[@class='tit']").text.split('#')[1]
    #             break
    #         else:
    #             driver.refresh()
    #             login_with_metamask()

    #     except:
    #         print("Page not fully loaded... i think")
    #         time.sleep(2)
    #         continue
    
    ship_class = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]").text
    ship_durability = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]").text.split(' / ')[0]
    ship_owner = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/a/div").text
   
    ship_attr_space = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]").text
    ship_attr_speed = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]").text
    ship_attr_skill = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]").text
    ship_attr_defence = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[4]/div[2]").text
    ship_attr_attack = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[5]/div[2]").text
    ship_attr_morale = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[6]/div[2]").text

    ship_parts_keel = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]").text
    ship_parts_sail = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]").text
    ship_parts_side = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/div[3]/div[2]").text
    ship_parts_bow = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/div[4]/div[2]").text
    ship_parts_cabin = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/div[5]/div[2]").text
    ship_parts_stern = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/div[6]/div[2]").text

    statsList = [transaction_id, ship_id, ship_class, ship_durability, ship_owner, \
        ship_attr_space, ship_attr_speed, ship_attr_skill, ship_attr_defence, ship_attr_attack, ship_attr_morale, \
        ship_parts_keel, ship_parts_sail, ship_parts_side, ship_parts_bow, ship_parts_cabin, ship_parts_stern, \
        ship_sold_price]

    return ','.join(map(str, statsList)) 




# If the initial export script has been run, then set this to True. Only delta will be needed
sold_already_exported = False
filename = 'db/extracted_sold_BNB.csv'
num_lines = sum(1 for line in open(filename))

# Create dataframe sold DF
header = ['transaction_id', 'ship_id', 'ship_class', 'ship_durability', 'ship_owner', \
        'ship_attr_space', 'ship_attr_speed', 'ship_attr_skill', 'ship_attr_defence', 'ship_attr_attack', 'ship_attr_morale', \
        'ship_parts_keel', 'ship_parts_sail', 'ship_parts_side', 'ship_parts_bow', 'ship_parts_cabin', 'ship_parts_stern', \
        'ship_sold_price']

sold_df = pd.DataFrame(columns=header)


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

driver = webdriver.Chrome('tools\chromedriver.exe',options=opt)

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

# Open marketplace
time.sleep(5)
driver.get(MARKET_URL)
time.sleep(2)

login_with_metamask()

# Get Metamask window
driver.switch_to.window(driver.window_handles[2])
driver.find_element_by_xpath('//button[text()="Next"]').click()
time.sleep(0.5)
driver.find_element_by_xpath('//button[text()="Connect"]').click()
time.sleep(0.5)

# Get cryptobay page 
driver.switch_to.window(driver.window_handles[0])

# Select "Marketplace" tab
driver.find_element_by_xpath('/html/body/div/div/header/div/div[1]/div/a[3]').click()

# Select "Dashboard" tab
driver.find_element_by_xpath('/html/body/div/div/header/div/div[1]/div/a[1]').click()



get_initial_sold_from_marketplace(False)

###TEMP
# while True: 
#     time.sleep(10)

driver.quit()