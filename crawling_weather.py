from datetime import datetime  # 이 줄을 추가해주세요

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def dateReader(date_):
    parts = date_.split(',', 2)
    date_string_modified = parts[0] + ',' + parts[1]
    date_object = datetime.strptime(date_string_modified, "%A, %d %B %Y")
    year = date_object.year
    month = date_object.month
    day = date_object.day
    return year, month, day


def dataReaderKorean(date_):
    parts = date_.split(' — ', 2)
    date_string_modified = parts[0]
    date_, time_ = date_string_modified.split(', ')

    date_object = datetime.strptime(date_, "%Y년 %m월 %d일 %A")

    year = date_object.year
    month = date_object.month
    day = date_object.day

    return year, month, day


def dateSelector(browser_, sel_date_, index_):
    selmonth = Select(browser_.find_element(By.CSS_SELECTOR, "div.tb-select select#month"))
    selmonth.select_by_index(index_)

    firstyear_datelist = browser_.find_elements(By.CSS_SELECTOR, "div.weatherLinks a")
    for i in firstyear_datelist:
        # print(i.text)
        try:
            find_date = datetime.strptime(i.text, "%a, %d %b")
        except ValueError:
            print("Invalid date format. Skipping...")
            break
        # print(f"sel_date {sel_date_.year}-{sel_date_.month}-{sel_date_.day}")
        # print(f"find_date {find_date.year}-{find_date.month}-{find_date.day}")

        if (sel_date_.month == find_date.month) and (sel_date_.day == find_date.day):
            print(f"date is found {find_date.month}-{find_date.day}")
            i.click()
            break


def crwalingweather(city, sel_date):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_argument("headless")
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36")
    options.add_argument("lang=en")
    options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )
    options.page_load_strategy = 'eager'
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.timeanddate.com/weather/south-korea/seoul")

    input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.bn-header__searchbox.picker-city.noprint input"))
    )
    input.send_keys(city)

    button = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.picker-city__button"))
    )
    button.click()

    time.sleep(0.5)
    href = browser.find_element(By.CSS_SELECTOR, "table.zebra.fw.tb-theme a").get_attribute("href")
    browser.get(href)

    time.sleep(0.5)
    pastweather = browser.find_elements(By.CSS_SELECTOR, "section.layout-grid__hero.tpl-banner__hero a")
    href_pastweather = pastweather[3].get_attribute("href")

    browser.get(href_pastweather)
    time.sleep(0.5)
    cur_date = browser.find_element(By.CSS_SELECTOR, "div.weatherTooltip div.date")
    print(f'cur city : {cur_date.text} ')
    cur_year, cur_month, cur_day = dateReader(cur_date.text)

    print(f"year : {cur_year}, month : {cur_month}, day : {cur_day}")

    move_index = 0

    # cur_year 2023 08
    # sel_year 2023 05
    # 현재같은 년도
    if cur_year <= sel_date.year:
        print("same year")
        move_index = cur_month - sel_date.month + 1
    # 과거
    else:
        print(f"past year {(cur_year - sel_date.year)}")
        move_index += (cur_year - sel_date.year) * 12
        move_index += cur_month - sel_date.month + 1

    # 1년 전 data
    dateSelector(browser, sel_date, move_index)
    time.sleep(0.5)

    one_year_ago_temp = browser.find_element(By.CSS_SELECTOR, "div.tempblock div.temp").text
    one_year_ago_wdesc = browser.find_element(By.CSS_SELECTOR, "div.tempblock div.wdesc").text
    print(one_year_ago_temp)
    print(one_year_ago_wdesc)
    time.sleep(0.5)

    # 2년 전 data

    dateSelector(browser, sel_date, move_index + 12)
    time.sleep(0.5)

    two_year_ago_temp = browser.find_element(By.CSS_SELECTOR, "div.tempblock div.temp").text
    two_year_ago_wdesc = browser.find_element(By.CSS_SELECTOR, "div.tempblock div.wdesc").text
    print(two_year_ago_temp)
    print(two_year_ago_wdesc)

    # 2년 전 data
    time.sleep(0.5)

    dateSelector(browser, sel_date, move_index + 24)
    time.sleep(0.5)

    three_year_ago_temp = browser.find_element(By.CSS_SELECTOR, "div.tempblock div.temp").text
    three_year_ago_wdesc = browser.find_element(By.CSS_SELECTOR, "div.tempblock div.wdesc").text
    print(three_year_ago_temp)
    print(three_year_ago_wdesc)
    time.sleep(0.5)

    return {
        'one_year_ago_temp': one_year_ago_temp,
        'one_year_ago_wdesc': one_year_ago_wdesc,
        'two_year_ago_temp': two_year_ago_temp,
        'two_year_ago_wdesc': two_year_ago_wdesc,
        'three_year_ago_temp': three_year_ago_temp,
        'three_year_ago_wdesc': three_year_ago_wdesc,
    }


def test_code():
    test_date = "2022-01-05"
    parse_date = datetime.strptime(test_date, "%Y-%m-%d")
    crwalingweather("seoul", parse_date)

# test_code()
