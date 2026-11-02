import pytest

from config import PASSWORD, USERNAME
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

BACKPACK = "sauce-labs-backpack"


def open_products(driver, username):
    LoginPage(driver).open().login(username, PASSWORD)
    return ProductsPage(driver)


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="problem_user: кнопка Remove не убирает товар (известный баг учебного сайта)",
)
def test_problem_user_remove_from_cart_known_bug(driver):
    products = open_products(driver, "problem_user")
    products.add_to_cart(BACKPACK)

    products.remove_from_cart(BACKPACK)

    assert products.get_cart_count() == 0


def test_sort_products_by_name_z_to_a(driver):
    products = open_products(driver, USERNAME)

    products.select_sort("za")

    names = products.get_product_names()
    assert names == sorted(names, reverse=True)
