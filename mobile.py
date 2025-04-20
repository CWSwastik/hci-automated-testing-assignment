# Note: the amazon app should be open before running this script as it doesn't accept permissions, login etc..

import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

class Stopwatch:
    def __init__(self):
        self.start_time = time.time()
        self.last_checkpoint = self.start_time

    def checkpoint(self, name: str):
        current_time = time.time()
        total = current_time - self.start_time
        partial = current_time - self.last_checkpoint
        self.last_checkpoint = current_time
        print(f"{name} took {total}s total, {partial}s from last checkpoint")


capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='in.amazon.mShop.android.shopping',
    appActivity='com.amazon.mShop.home.HomeActivity',
    language='en',
    locale='US',
    noReset=True,
)

appium_server_url = 'http://localhost:4723'
driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
driver.implicitly_wait(10)


# search for the required item
def search(query: str):
    # enter the search screen
    driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="in.amazon.mShop.android.shopping:id/chrome_search_hint_view"]').click()
    search_bar = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@resource-id="in.amazon.mShop.android.shopping:id/rs_search_src_text"]')
    search_bar.send_keys(query)
    driver.press_keycode(66)  # press enter

# open filters page and sort by the given checkbox id
def sort_by(checkbox_id: str):
    # open filters page
    driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@resource-id="s-all-filters-announce"]').click()

    # scroll to sort by button
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollForward(3).scrollIntoView(new UiSelector().textContains("Sort By").instance(0))')
    # for some reason click another button in the list before clicking sorting by
    driver.find_element(AppiumBy.XPATH, '//android.view.View[@text="Availability"]').click()
    driver.find_element(AppiumBy.XPATH, '//android.view.View[@text="Sort by"]').click()
    # choose your sorting option
    driver.find_element(AppiumBy.XPATH, f'//android.widget.CheckBox[@resource-id="sort/{checkbox_id}-rank"]').click()
    # wait for it to complete loading
    time.sleep(2)
    # exit the filters page
    driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="close"]').click()

def element_exists(xpath: str):
    if len(driver.find_elements(AppiumBy.XPATH, xpath)) > 0:
        return True
    return False

# get the topmost product details
def topmost_product_details():
    parent_xpath = '//android.view.View[@resource-id="search"]/android.view.View[5]/android.view.View[1]/android.view.View[1]'
    if not element_exists(parent_xpath):
        parent_xpath = '//android.widget.ListView/android.view.View[1]/android.view.View[1]/android.view.View[1]'
    title = driver.find_element(AppiumBy.XPATH, f'{parent_xpath}/android.view.View[2]/android.widget.TextView[1]').text
    price = driver.find_element(AppiumBy.XPATH, f'{parent_xpath}/android.view.View[3]/android.widget.TextView[3]').text
    return title, price

# use this to ensure stuff is visible on the screen to be interacted with
def scroll_y(by: int):
    rect = driver.get_window_rect()
    x = rect['width'] / 2
    y = rect['height'] / 2
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y - by).pointer_down().move_to_location(x, y + by).release()
    actions.perform()


try:
    stopwatch = Stopwatch()
    search('wireless headphones')
    stopwatch.checkpoint('a')

    time.sleep(1)
    sort_by('price-asc')
    time.sleep(1)
    scroll_y(-300)
    time.sleep(1)
    name, price = topmost_product_details()
    print(f"Lowest price product: {name}: {price}")
    stopwatch.checkpoint('b')

    scroll_y(300)
    sort_by('review')
    time.sleep(1)
    scroll_y(-200)
    name, price = topmost_product_details()
    print(f"Lowest price product: {name}: {price}")
    stopwatch.checkpoint('c')

    cart_button = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Add to cart").instance(0)')
    cart_button.click()
    stopwatch.checkpoint('d')
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    driver.quit()
