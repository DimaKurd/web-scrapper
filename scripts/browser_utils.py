from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Worker:

    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x1080')

        self.driver = webdriver.Chrome(chrome_options=options)  # WebDriver Initialization
        self.driver.implicitly_wait(3)
        self.actions = ActionChains(self.driver)
        self.driver.get(url)
        self.search_line = self.driver.find_element(By.XPATH, '//input')
        self.wait = WebDriverWait(self.driver, 5)

    def enter_new_address(self, address):
        self.search_line.send_keys(address)
        self.driver.find_element(By.XPATH, '//button[contains(@class,"_view_search")]').click()
        sleep(3)

    def empty_search_line(self):
        self.search_line.send_keys(Keys.CONTROL + 'a', Keys.DELETE)

    def click_on_orgs_inside_button(self):
        orgs_inside = self.driver.find_element(By.XPATH, '//div[contains(@class,"_name_inside")]')
        orgs_inside.click()

    def open_org_card(self, i):
        # trying to find new organization card
        org = self.driver.find_element(By.XPATH,
                                       '//div[contains(@class,"card-businesses-list__list")]/div[{}]'.format(i))
        # sleep(3)
        try:
            self.actions.move_to_element(org).perform()
        except ElementNotInteractableException:
            return ElementNotInteractableException

        try:
            org.click()
        except ElementClickInterceptedException:
            return ElementClickInterceptedException
        except ElementNotInteractableException:
            return ElementNotInteractableException
        return self.driver.find_element(By.XPATH, '//h1/div/a').text

    def click_on_reviews_button(self):
        actions = ActionChains(self.driver)
        try:
            next_button = self.driver.find_element(By.XPATH,
                                                   '//div[contains(@class,"tabs-select-view__titles")]//div[contains(@class,"_next")]')
            actions.move_to_element(next_button).perform()
            next_button.click()
        except NoSuchElementException:
            pass
        reports = self.driver.find_element(By.XPATH, '//div[contains(@class,"_name_reviews")]')
        actions.move_to_element(reports).perform()
        reports.click()
        # sleep(2)

    def get_review(self, j):

        review = self.wait.until(lambda d: d.find_element(By.XPATH,
                                                          '(//span[contains(@class,"business-review-view__body-text")])[{}]'.format(
                                                              j)))
        # self.actions.move_to_element(review).perform()

        self.actions.send_keys(Keys.PAGE_DOWN).perform()
        return review.text

    def close_ads(self):
        try:
            self.driver.find_element(By.XPATH, '//*[local-name()="svg" and @viewBox="0 0 14 14"]').click()
        except NoSuchElementException:
            pass

    def back(self):
        self.driver.back()

    def get_review_mark(self, j):
        self.driver.implicitly_wait(0)
        try:
            for i in range(1, 6):
                self.driver.find_element(By.XPATH,
                                         '(//div[contains(@class,"business-review-view__rating")])[{}]/span/div/span['
                                         'contains(@class, "_empty")][{}] '.format(j, i))
        except NoSuchElementException:
            pass
        finally:
            self.driver.implicitly_wait(3)
            return 6 - i
        # (//div[contains(@class,"business-review-view__rating")])[6]/span/div/span[contains(@class, "_empty")]
