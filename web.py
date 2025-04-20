import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Timer:
    def __init__(self):
        self._start_time = None
        self._end_time = None   

    def start(self):
        self._start_time = time.perf_counter()
        self._end_time = None

    def stop(self):
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")
        self._end_time = time.perf_counter()
        return (self._end_time - self._start_time) * 1000  # ms

    def elapsed(self):
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")
        return (time.perf_counter() - self._start_time) * 1000  # ms


def main():
    timer = Timer()
    link = "https://www.amazon.in/"
    options = webdriver.ChromeOptions()
    options.add_argument(
        r"--user-data-dir=C:\Users\cwswa\AppData\Local\Google\Chrome\User Data"
    )

    driver = webdriver.Chrome()
    timer.start()
    driver.get(link)
    res = timer.stop()
    print(f"(f) The load time for the home page is {res} ms.")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )  # Wait for captcha to be solved if present

    timer.start()
    inputElement = driver.find_element(By.ID, "twotabsearchtextbox")
    inputElement.send_keys("wireless headphones" + Keys.ENTER)
    res = timer.stop()

    print(f"(a) The response time for searching headphones is {res} ms.")

    # Sort by price

    timer.start()
    sortByElement = driver.find_element(By.ID, "s-result-sort-select")
    sortByElementSelect = Select(sortByElement)
    sortByElementSelect.select_by_visible_text("Price: Low to High")
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
        )
    )

    lowestPriceProd = None
    lowestPriceProdTitle = None
    lowestPriceProdPrice = None
    for prod in results:
        try:
            # Try to locate the title and price elements, if not found, go to next product
            title = prod.find_element(By.CSS_SELECTOR, ".a-size-medium")
            price = prod.find_element(By.CSS_SELECTOR, ".a-price-whole")
            lowestPriceProd = prod
            lowestPriceProdTitle = title
            lowestPriceProdPrice = price
            break
        except Exception:
            continue
    if not lowestPriceProd:
        raise Exception("No product with a price found.")
    res = timer.stop()

    print("Lowest price product: " + lowestPriceProdTitle.text)
    print("Lowest price product price: " + lowestPriceProdPrice.text)

    print(f"(b) The response time for finding lowest priced item is {res} ms.")

    # Sort by rating

    timer.start()
    sortByElement = driver.find_element(By.ID, "s-result-sort-select")
    sortByElementSelect = Select(sortByElement)
    sortByElementSelect.select_by_visible_text("Avg. Customer Review")

    resultItems = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
        )
    )

    highestRatedProd = None
    highestRatedProdTitle = None
    highestRatedProdPrice = None

    for prod in resultItems:
        try:
            title = prod.find_element(By.CSS_SELECTOR, ".a-size-medium")
            price = prod.find_element(By.CSS_SELECTOR, ".a-price-whole")
            highestRatedProd = prod
            highestRatedProdTitle = title
            highestRatedProdPrice = price
            break
        except Exception:
            continue
    if highestRatedProd is None:
        raise Exception("No product with a price found.")
    res = timer.stop()
    print("Highest rated product: " + highestRatedProdTitle.text)
    print("Highest rated product price: " + highestRatedProdPrice.text)

    print(f"(c) The response time for finding Highest rated item is {res} ms.")

    # Add to cart

    timer.start()
    addToCartButton = highestRatedProd.find_element(By.CLASS_NAME, "a-button-text")
    addToCartButton.click()
    res = timer.stop()

    print(f"(d) The response time for adding the item to cart is {res} ms.")

    driver.quit()


if __name__ == "__main__":
    main()
