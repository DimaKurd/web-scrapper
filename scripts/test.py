from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from browser_utils import *
from pandas_utils import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('doc_name', help='name of document from data folder')
parser.add_argument('left_border', help='left edge of addresses')
parser.add_argument('right_border', help='right edge of addresses')
parser.add_argument('output', help='name of output file')
args = parser.parse_args()


data = Data(args.output)
# closing ads banner

# start iterating over addresses
adresses = data.get_addresses_from_data('../data/{}'.format(args.doc_name))[
           int(args.left_border):int(args.right_border)]
# print(adresses)
for address in adresses:
    worker = Worker('https://yandex.ru/maps')
    worker.close_ads()
    worker.enter_new_address(address)  # enter new address
    try:
        worker.click_on_orgs_inside_button()  # open organizations inside button
        i = 1
        # start iterating over organizations inside building
        while True:
            try:
                org_name = worker.open_org_card(i)  # opening new organization card
                try:
                    worker.click_on_reviews_button()  # open reviews
                    j = 1
                    while True:
                        try:
                            review_text = worker.get_review(j)
                            review_score = worker.get_review_mark(j)
                            data.add_new_line(address, org_name, review_text, review_score)
                            j += 1
                        except NoSuchElementException:
                            print(j)
                            break
                        except TimeoutException:
                            print(j)
                            break
                except NoSuchElementException:  # no reviews
                    pass
                except ElementClickInterceptedException:
                    pass
                except ElementNotInteractableException:
                    pass
                # data.save_progress(args.output)
                worker.back()
                # sleep(1)
                i += 1
            except NoSuchElementException:  # no more organizations
                break
        worker.empty_search_line()
    except NoSuchElementException:
        worker.empty_search_line()
        continue
    worker.driver.quit()
# data.save_progress('test')
