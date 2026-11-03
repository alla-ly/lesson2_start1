from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from config import TIMEOUT


class ProductsPage:
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    SORT_SELECT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def get_title(self):
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def get_product_names(self):
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        return [element.text for element in self.driver.find_elements(*self.PRODUCT_NAMES)]

    # product_slug — часть id кнопки, например "sauce-labs-backpack"
    def add_to_cart(self, product_slug):
        button = (By.ID, f"add-to-cart-{product_slug}")
        self.wait.until(EC.element_to_be_clickable(button)).click()

    def remove_from_cart(self, product_slug):
        button = (By.ID, f"remove-{product_slug}")
        self.wait.until(EC.element_to_be_clickable(button)).click()

    def is_remove_button_visible(self, product_slug):
        button = (By.ID, f"remove-{product_slug}")
        return self.wait.until(EC.visibility_of_element_located(button)).is_displayed()

    def get_cart_count(self):
        # бейджа нет в DOM, пока корзина пуста — это не ошибка, а 0
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()

    def select_sort(self, value):
        # <select> перерисовывается после выбора, поэтому каждый раз ищем его заново
        select = self.wait.until(EC.presence_of_element_located(self.SORT_SELECT))
        Select(select).select_by_value(value)
