import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password
from helper import add_pets_with_photo, delete_all_pets
import time

# создаем список питомцев пользователя
for _ in range(10):
    add_pets_with_photo()


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    # ожидание
    pytest.driver.implicitly_wait(10)

    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(by=By.ID, value='email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(by=By.ID, value='pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
    # Нажимаем на кнопку отображения птомцев пользователя
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='a.nav-link[href="/my_pets"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(by=By.CSS_SELECTOR, value='h2').text == "limbo"
    # Проверяем что присутствуют все питомцы
    assert len(pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr')) == \
           int(pytest.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[1]').text.split()[2])


def test_pet_foto():
    pets_with_foto = int()
    # Вводим email
    pytest.driver.find_element(by=By.ID, value='email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(by=By.ID, value='pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
    # Нажимаем на кнопку отображения птомцев пользователя
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='a.nav-link[href="/my_pets"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(by=By.CSS_SELECTOR, value='h2').text == "limbo"
    # Проверяем что хотя бы у половины питомцев есть фото
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody>tr'))
    )
    for pet in pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr'):
        if pet.find_element(By.CSS_SELECTOR, value='th>img').get_attribute('src'):
            pets_with_foto += 1
    assert pets_with_foto >= len(pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr')) - pets_with_foto


def test_pet_names_breed_age():
    # Вводим email
    pytest.driver.find_element(by=By.ID, value='email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(by=By.ID, value='pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
    # Нажимаем на кнопку отображения птомцев пользователя
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='a.nav-link[href="/my_pets"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(by=By.CSS_SELECTOR, value='h2').text == "limbo"
    # Проверяем что у всех питомцев есть имя, возраст и порода
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody>tr'))
    )
    for pet in pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr'):
        for i in pet.find_elements(By.CSS_SELECTOR, value='td:not(.smart_cell)'):
            assert len(i.text) > 0


def test_pet_names():
    names = set()
    # Вводим email
    pytest.driver.find_element(by=By.ID, value='email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(by=By.ID, value='pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
    # Нажимаем на кнопку отображения птомцев пользователя
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='a.nav-link[href="/my_pets"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(by=By.CSS_SELECTOR, value='h2').text == "limbo"
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody>tr'))
    )
    # Проверяем что у всех питомцев разные имена
    for pet in pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr'):
        names.add(pet.find_elements(by=By.CSS_SELECTOR, value='td')[0].text)
    assert len(names) == len(pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr'))


def test_unic_pets():
    pets = []
    # Вводим email
    pytest.driver.find_element(by=By.ID, value='email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(by=By.ID, value='pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
    # Нажимаем на кнопку отображения птомцев пользователя
    pytest.driver.find_element(by=By.CSS_SELECTOR, value='a.nav-link[href="/my_pets"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(by=By.CSS_SELECTOR, value='h2').text == "limbo"
    # Проверяем что в списке нет повторяющихся питомцев
    for pet in pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr'):  # Создание списка питомцев
        pets.append({'foto': pet.find_element(By.CSS_SELECTOR, value='th>img').get_attribute('src'),
                     'name': pet.find_elements(By.CSS_SELECTOR, value='td:not(.smart_cell)')[0].text,
                     'bred': pet.find_elements(By.CSS_SELECTOR, value='td:not(.smart_cell)')[1].text,
                     'age': pet.find_elements(By.CSS_SELECTOR, value='td:not(.smart_cell)')[2].text
                     })
    for i, pet_main in enumerate(pets):  # Сравнение питомцев
        num = i
        for pet_comparison in pets[num + 1::]:
            assert (pet_main['foto'] != pet_comparison['foto'] or \
                    pet_main['name'] != pet_comparison['name'] or \
                    pet_main['bred'] != pet_comparison['bred'] or \
                    pet_main['age'] != pet_comparison['age'])
            num += 1


# удаление питомцев
def test_teardown():
    delete_all_pets()
