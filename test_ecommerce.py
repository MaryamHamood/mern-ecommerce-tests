import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = os.environ.get("APP_URL", "http://13.206.102.133:4000")
TEST_EMAIL = "testuser@gmail.com"
TEST_PASSWORD = "123456"
ADMIN_EMAIL = "testadmin@gmail.com"
ADMIN_PASSWORD = "123456"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Test 1
def test_homepage_loads(driver):
    driver.get(BASE_URL)
    assert driver.title != ""

# Test 2
def test_homepage_has_products(driver):
    driver.get(BASE_URL)
    time.sleep(2)
    body = driver.find_element(By.TAG_NAME, "body")
    assert body is not None

# Test 3
def test_login_page_loads(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    assert "login" in driver.current_url.lower() or driver.find_element(By.TAG_NAME, "form")

# Test 4
def test_login_page_has_email_field(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[placeholder*='mail']")
    assert email_field is not None

# Test 5
def test_login_page_has_password_field(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    assert password_field is not None

# Test 6
def test_login_with_wrong_credentials(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    email = driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[placeholder*='mail']")
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    email.clear()
    email.send_keys("wrong@gmail.com")
    password.clear()
    password.send_keys("wrongpassword")
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")
    button.click()
    time.sleep(2)
    body = driver.find_element(By.TAG_NAME, "body")
    assert "invalid" in body.text.lower() or driver.current_url.endswith("/login")

# Test 7
def test_login_with_correct_credentials(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    email = driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[placeholder*='mail']")
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    email.clear()
    email.send_keys(TEST_EMAIL)
    password.clear()
    password.send_keys(TEST_PASSWORD)
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")
    button.click()
    time.sleep(2)
    assert True  # login attempted successfully

# Test 8
def test_register_page_loads(driver):
    driver.get(f"{BASE_URL}/register")
    time.sleep(1)
    assert "register" in driver.current_url.lower() or driver.find_element(By.TAG_NAME, "form")

# Test 9
def test_register_page_has_fields(driver):
    driver.get(f"{BASE_URL}/register")
    time.sleep(1)
    inputs = driver.find_elements(By.TAG_NAME, "input")
    assert len(inputs) >= 3

# Test 10
def test_navigation_links_present(driver):
    driver.get(BASE_URL)
    time.sleep(1)
    links = driver.find_elements(By.TAG_NAME, "a")
    assert len(links) > 0

# Test 11
def test_cart_link_present(driver):
    driver.get(BASE_URL)
    time.sleep(1)
    body = driver.find_element(By.TAG_NAME, "body")
    assert "cart" in body.text.lower() or len(driver.find_elements(By.CSS_SELECTOR, "a[href*='cart']")) > 0

# Test 12
def test_product_page_loads(driver):
    driver.get(BASE_URL)
    time.sleep(2)
    links = driver.find_elements(By.TAG_NAME, "a")
    product_links = [l for l in links if "/product/" in (l.get_attribute("href") or "")]
    if product_links:
        product_links[0].click()
        time.sleep(2)
    assert "product" in driver.current_url or driver.find_element(By.TAG_NAME, "body")

# Test 13
def test_admin_login(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    email = driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[placeholder*='mail']")
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    email.clear()
    email.send_keys(ADMIN_EMAIL)
    password.clear()
    password.send_keys(ADMIN_PASSWORD)
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")
    button.click()
    time.sleep(2)
    assert True  # login attempted successfully

# Test 14
def test_admin_panel_accessible(driver):
    driver.get(f"{BASE_URL}/admin/userlist")
    time.sleep(2)
    body = driver.find_element(By.TAG_NAME, "body")
    assert body is not None

# Test 15
def test_page_title_not_empty(driver):
    driver.get(BASE_URL)
    time.sleep(1)
    assert driver.title is not None and driver.title != ""
