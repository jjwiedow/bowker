from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import datetime


driver = webdriver.Chrome(executable_path="C:/Users/steps/Desktop/chromedriver.exe")
driver.get("https://www.bowkerlink.com/corrections/common/home.asp")


def find_by_xpath(locator):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, locator))
    )
    return element


class LoginPage(object):
    def input_login(self, login_cred):
        find_by_xpath('//input[@name = "username"]').send_keys(login_cred['username'])
        find_by_xpath('//input[@name = "password"]').send_keys(login_cred['password'])
        return self

    def login_click(self) -> object:
        find_by_xpath('//input[@value = "Login"]').click()


class FormPage(object):
    def fill_form(self, data):
        find_by_xpath('//input[@name = "item_#isbn"]').send_keys(isbn)
        find_by_xpath('//input[@name = "title_#title"]').send_keys(prod)
        find_by_xpath('//input[@name = "contrib_#0#0#name_sort"]').send_keys(form_data['company'])
        find_by_xpath('//input[@name = "market_#0#pub_date"]').send_keys(form_data['pub_date'])
        find_by_xpath('//input[@name = "price_#0#0#1#price"]').send_keys(form_data['price'])
        find_by_xpath('//td/select/option[@value = "348"]').click()  # binding
        find_by_xpath('//td/select/option[@value = "47617"]').click()  # subject
        find_by_xpath('//td/select/option[@value = "14"]').click()  # contributor
        find_by_xpath('//td/input[@name = "chkbox_contrib_#0#0#corporate_ind"]').click()  # company check
        find_by_xpath('//td/select[@name = "price_#0#0#1#rc_price_type_uid"]/option[@value = "12"]').click()  # price type
        find_by_xpath('//td/select/option[@value = "902"]').click()  # currency
        find_by_xpath('//td/select/option[@value = "805"]').click()  # target market

        return self

    def submit(self):
        find_by_xpath('//a[@href = "javascript:SaveChanges();"]').click()


login_cred = {
    'username': 'StepstoLiteracy',
    'password': '4EasyStreet!'
}

form_data = {
    'company': 'Steps To Literacy',
    'pub_date': '2019',
    'price': '10000'
}

filename = 'C:/Users/steps/Desktop/Bowker/isbn_data.csv'

isbn_data = []
description_data = []

with open(filename, 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    for num, row in enumerate(reader, start=1):
        isbn_data.append(row['ISBN'])
        description_data.append(row['Product Description'])

n = 0
max_rows = len(isbn_data)

while True:
    LoginPage().input_login(login_cred)
    LoginPage().login_click()
    if driver.current_url == "https://www.bowkerlink.com/corrections/common/home.asp":
        print("Login Success")
        while n < max_rows:
            isbn = isbn_data[n]
            prod = description_data[n]
            try:
                find_by_xpath('//a[@href = "/corrections/bip/bl_ItemEdit.asp"]').click()
                FormPage().fill_form(form_data).submit()
                with open('bowkerlog.txt', 'a') as log:
                    dt = str(datetime.datetime.now())
                    log.write(isbn + ', ' + prod + ', ' + dt + '\n')
                n += 1
            except ValueError as e:
                print('There was a problem entering {}.'.format(isbn))
    else:
        print("Login Failed")
        break

