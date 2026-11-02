import pytest

from config import PASSWORD, USERNAME
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_standard_user_can_login(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)

    products = ProductsPage(driver)

    assert products.get_title() == "Products"
    assert len(products.get_product_names()) == 6


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", PASSWORD, "Epic sadface: Sorry, this user has been locked out."),
        ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
        ("", PASSWORD, "Epic sadface: Username is required"),
    ],
    ids=["locked_out_user", "wrong_password", "empty_username"],
)
def test_login_negative(driver, username, password, expected_error):
    login_page = LoginPage(driver).open()

    login_page.login(username, password)

    assert login_page.get_error_text() == expected_error
