import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome("C:\SeleniumChrome\chromedriver.exe")
    pytest.driver.get("https://petfriends.skillfactory.ru/login")
    yield
    pytest.driver.quit()


def test_show_my_pets():
    pytest.driver.find_element_by_id('email').send_keys('afevraleff@ya.ru')
    pytest.driver.find_element_by_id('pass').send_keys('regkoj-dadba5-qIztuc')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    pytest.driver.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Неявное ожидание
    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements_by_css_selector('th[scope="row"] > img')
    names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    species = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    ages = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    # Явные ожидания элементов
    WebDriverWait(pytest.driver, 10).until(EC.title_is("PetFriends: My Pets"))
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]")))
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody')))
    # Извлекаем поле со статистикой
    quantity = pytest.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]')
    with_photo = []
    setNames = set()
    summList = []
    a = ()
    for i in range(len(names)):
        # Карточек с фото больше чем карточек без фото
        if images[i].get_attribute('src') != "https://petfriends.skillfactory.ru/static/images/upload2.jpg":
            with_photo.append(1)
        setNames.add(names[i].get_attribute('innerText'))
        a = (names[i].get_attribute('innerText'), species[i].get_attribute('innerText'),
                       ages[i].get_attribute('innerText'), images[i].get_attribute('src'))
        summList.append(a)
        # Заполненность всех полей
        assert names[i].get_attribute('innerText') != ""
        assert species[i].get_attribute('innerText') != ""
        assert ages[i].get_attribute('innerText') != ""
    #Из поля со статистикой извлекаем количество питомцев
    prepQuan = quantity.text.split('\n')[1].split(" ")[1]
    # Количество питомцев с фото
    assert len(with_photo) * 2 > len(names)
    # Соответствие количества карточек количеству питомцев в статистике
    assert prepQuan == str(len(names))
    # Нет повторяющихся питомцев
    assert len(names) == len(set(summList))
    # Нет повторяющихся имен
    assert len(names) == len(setNames)
