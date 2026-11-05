import allure

from config import PASSWORD, USERNAME
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

BACKPACK = "sauce-labs-backpack"


def test_add_product_to_cart(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    products = ProductsPage(driver)

    products.add_to_cart(BACKPACK)

    assert products.is_remove_button_visible(BACKPACK)
    assert products.get_cart_count() == 1


@allure.title("Backpack is in cart after add")
def test_backpack_is_in_cart(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    products = ProductsPage(driver)

    products.add_to_cart(BACKPACK)
    with allure.step("Open cart"):
        products.open_cart()

    assert "Sauce Labs Backpack" in products.get_product_names()


def test_remove_product_from_cart(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    products = ProductsPage(driver)
    products.add_to_cart(BACKPACK)

    products.remove_from_cart(BACKPACK)

    assert products.get_cart_count() == 0
