import platform
import os
from datetime import date, datetime
from itertools import islice
from typing import Dict, List, Any, Union

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

WebDriver = webdriver.Firefox

SHORT_TIMEOUT: int = 15
LONG_TIMEOUT: int = 30


def calendar_handler(driver: WebDriver, dt: date, xpath: str, tb_xpath: str) -> None:
    """
    Handles the calendar pop-up and clicks on
    the proper date given in the dt
    """

    WebDriverWait(driver, timeout=SHORT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.find_element(By.XPATH, xpath).click()

    core: str = xpath.split('_')[0]
    received_data: str
    year: str = '0'
    while int(year) != dt.year:
        received_data = driver.find_element(By.XPATH, core + '_DDD_C_T"]').text
        year = received_data.split(' ')[1]

        if int(year) > dt.year:
            driver.find_element(By.XPATH, core + '_DDD_C_PYCImg"]').click()
        elif int(year) < dt.year:
            driver.find_element(By.XPATH, core + '_DDD_C_NYCImg"]').click()

    converted_month: int = 0
    while converted_month != dt.month:
        received_data = driver.find_element(By.XPATH, core + '_DDD_C_T"]').text
        month: str = received_data.split(' ')[0]
        converted_month = datetime.strptime(month, '%B').month

        if converted_month > dt.month:
            driver.find_element(By.XPATH, core + '_DDD_C_PMCImg"]').click()
        elif converted_month < dt.month:
            driver.find_element(By.XPATH, core + '_DDD_C_NMCImg"]').click()

    tbody: WebElement = driver.find_element(By.XPATH, tb_xpath)
    rows: List[WebElement] = tbody.find_elements(By.TAG_NAME, 'tr')
    row: WebElement
    column: WebElement

    for row in islice(rows, 1, None):
        for column in row.find_elements(By.TAG_NAME, 'td'):
            if 'dxeCalendarDay_Aqua' == column.get_attribute('class') and column.text == str(dt.day):
                column.click()
                break
        else:
            continue
        break


def scrap(url: str) -> Union[List[Dict[str, str]], None]:
    """
    Scraps a schedule from the page given in the url for
    the whole term and returns it as a list
    """

    webdriver_path: str
    if platform.system() == 'Windows':
        webdriver_path = f'{os.getcwd()}/drivers/geckodriver.exe'
    elif platform.system() == 'Linux':
        webdriver_path = f'{os.getcwd()}/drivers/geckodriver-linux'
    else:
        webdriver_path = f'{os.getcwd()}/drivers/geckodriver'

    if not os.path.isfile(webdriver_path):
        print('[!] Path to webdriver is not correct')
        return None
    else:
        schedule: List[Dict[str, str]] = list(dict())
        driver: WebDriver = WebDriver(executable_path=webdriver_path)
        driver.get(url)
        try:
            WebDriverWait(driver, timeout=SHORT_TIMEOUT).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div/div[2]'))
            )
            driver.find_element(By.XPATH, '/html/body/div/div[1]/p').click()

            WebDriverWait(driver, timeout=SHORT_TIMEOUT).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/table[4]/tbody/tr[1]/td[2]/table/tbody/tr/td/div/a[2]'))
            )
            driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr[1]/td[2]/table/tbody/tr/td/div/a[2]').click()

            WebDriverWait(driver, timeout=SHORT_TIMEOUT).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="DataDo_I"]'))
            )
            today: date = date.today()
            date_from: date
            date_to: date

            if today >= date(today.year, 7, 1):
                date_from = date(today.year, 10, 1)
                date_to = date(today.year + 1, 2, 15)
            elif today <= date(today.year, 2, 15):
                date_from = date(today.year - 1, 10, 1)
                date_to = date(today.year, 2, 15)
            else:
                date_from = date(today.year, 2, 15)
                date_to = date(today.year, 7, 1)

            calendar_handler(driver, date_from, '//*[@id="DataOd_B-1"]', '/html/body/table[4]/tbody/tr[2]/td['
                                                                         '2]/div/div[2]/form/table/tbody/tr[2]/td['
                                                                         '2]/table''/tbody/tr['
                                                                         '2]/td/div/div/div/div/table[2]/tbody/tr['
                                                                         '1]/td/table/tbody/tr[2]/td/table/tbody')
            calendar_handler(driver, date_to, '//*[@id="DataDo_B-1"]', '/html/body/table[4]/tbody/tr[2]/td['
                                                                       '2]/div/div[2]/form/table/tbody/tr[2]/td['
                                                                       '2]/table/tbody/tr['
                                                                       '4]/td/div/div/div/div/table[2]/tbody/tr['
                                                                       '1]/td/table/tbody')
            driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr[2]/td[2]/div/div[2]/form/table/tbody/tr['
                                          '2]/td[3]/a').click()

            WebDriverWait(driver, timeout=LONG_TIMEOUT).until_not(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="gridViewPlanyGrup_custwindow_State"]'))
            )

        except TimeoutException:
            print('[!] Unable to find element after waiting few seconds.')
            driver.close()

        except NoSuchElementException:
            print('[!] Unable to find element, please wait for updated version of script.')
            driver.close()

        finally:
            html: str = driver.page_source
            driver.close()

            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', {'id': 'gridViewPlanyGrup_DXMainTable'})
            rows: List[Any] = table.find_all('tr')
            columns: List[Any]
            row: Any
            column: Any
            classes_date: str = ''

            for row in rows:
                if row.has_attr('class'):
                    columns = row.find_all('td')
                    if 'dxgvGroupRow_Aqua' in row['class']:
                        classes_date = columns[1].get_text().split(' ')[3]
                    else:
                        hour_from: str = columns[1].get_text().replace('\xa0', '')
                        hour_to: str = columns[2].get_text().replace('\xa0', '')
                        subject: str

                        if columns[5].get_text()[0] == 'L':
                            subject = 'W ' + columns[4].get_text().replace('\xa0', '')
                        elif columns[5].get_text()[0] == 'T':
                            subject = 'C ' + columns[4].get_text().replace('\xa0', '')
                        else:
                            subject = columns[5].get_text()[0] + ' ' + columns[4].get_text().replace('\xa0', '')

                        subject = ' '.join(subject.split())

                        classroom: str = columns[7].get_text().replace('\xa0', '')
                        if not classroom:
                            classroom = 'sala wirtualna'
                        else:
                            classroom = ', s.'.join(classroom.split())

                        teacher: str = columns[8].get_text().replace('\xa0', '')
                        teacher = ' '.join(teacher.split())

                        schedule.append(
                            {
                                'classes_date': classes_date,
                                'hour_from': hour_from,
                                'hour_to': hour_to,
                                'subject': subject,
                                'classroom': classroom,
                                'teacher': teacher
                            }
                        )

        return schedule
