import os
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tests.pages.main_page import MainPage
from tests.pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from urllib import parse
from config import EMAIL, PASSWORD

# 실행 결과 폴더 경로 설정
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

class TestMainPage:
    def test_open_main_page(self, driver: WebDriver):
        try:
            main_page = MainPage(driver)
            main_page.open()

            wait = ws(driver, 10)
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url

        except NoSuchElementException as e:
            driver.save_screenshot("./screenshots/메인페이지-실패-노서치.png")
            assert False

    def test_click_link_text(self, driver: WebDriver):
        try:
            main_page = MainPage(driver)
            main_page.open()

            wait = ws(driver, 10)
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url

            # 로그인 클릭
            main_page.click_by_LINK_TEXT('로그인')
            wait.until(EC.url_contains("login"))
            assert "login" in driver.current_url
            driver.save_screenshot("./screenshots/메인페이지-로그인-성공.png")

            driver.back()
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url

            # 회원가입 클릭
            main_page.click_by_LINK_TEXT('회원가입')
            wait.until(EC.url_contains("memberJoinFrm"))
            assert "memberJoinFrm" in driver.current_url
            driver.save_screenshot("./screenshots/메인페이지-회원가입-성공.png")

            driver.back()
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url

            # 마이쿠팡 클릭
            main_page.click_by_LINK_TEXT('마이쿠팡')
            wait.until(EC.url_contains("login"))
            assert "login" in driver.current_url
            driver.save_screenshot("./screenshots/메인페이지-장바구니-성공.png")

        except NoSuchElementException as e:
            driver.save_screenshot("./screenshots/메인페이지-링크텍스트-실패-노서치.png")
            assert False
        except TimeoutException as e:
            driver.save_screenshot("./screenshots/메인페이지-링크텍스트-실패-타임에러.png")
            assert False

    def test_search_items(self, driver: WebDriver):
        try:
            ITEMS_XPATH = "//form//ul/li"
            main_page = MainPage(driver)
            main_page.open()

            wait = ws(driver, 10)
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url

            # 검색어 입력
            main_page.search_items('노트북')

            ws(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ITEMS_XPATH))
            )

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            item_name = parse.quote('노트북')

            assert len(items) > 0
            assert item_name in driver.current_url

            driver.save_screenshot("./screenshots/메인페이지-검색-성공.png")
        except NoSuchElementException as e:
            driver.save_screenshot("./screenshots/메인페이지-검색-실패-노서치.png")
            assert False
        except TimeoutException as e:
            driver.save_screenshot("./screenshots/메인페이지-검색-실패-타임에러.png")
            assert False

    def test_login_functionality(self, driver: WebDriver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        wait = ws(driver, 10)

        login_page.open()
        main_page.click_by_LINK_TEXT('로그인')

        login_page.input_email_and_password(EMAIL, PASSWORD)

        time.sleep(3)

        # 로그인 버튼 클릭 후 대기
        try:
            login_page.submit_login()
        except Exception as e:
            print(f"로그인 버튼 클릭 실패: {e}")
            driver.save_screenshot("./screenshots/로그인-실패-버튼클릭불가.png")
            assert False

        # 로그인 후 페이지 이동 확인
        try:
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url
        except TimeoutException:
            driver.save_screenshot("./screenshots/로그인-실패-페이지이동안됨.png")
            print("로그인 실패: 쿠팡 메인 페이지로 이동하지 않음")
            assert False

        # 로그인 후 URL에 'login'이 포함되어 있지 않은지 확인
        if "login" in driver.current_url:
            driver.save_screenshot("./screenshots/로그인-실패-리디렉션문제.png")
            print("로그인 실패: 로그인 페이지로 리디렉션됨")
            assert False  # 로그인이 되지 않았다는 의미로 assert False 추가

        # 로그인 성공 여부 확인
        assert "login" not in driver.current_url

        # 특정 요소(메인 페이지 요소) 확인
        try:
            main_page_element = wait.until(EC.visibility_of_element_located((By.ID, "main-page-identifier")))
            driver.save_screenshot("./screenshots/로그인-성공.png")
        except TimeoutException:
            driver.save_screenshot("./screenshots/로그인-실패-메인요소없음.png")
            print("로그인 실패: 메인 페이지 요소 없음")
            assert False