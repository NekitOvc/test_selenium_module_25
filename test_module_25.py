import pytest

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
    # инициализация драйвера
    selenium = webdriver.Chrome()
    selenium.implicitly_wait(10)
    # переход на сайт
    selenium.get('https://petfriends.skillfactory.ru/login')

    yield selenium
    selenium.quit()

# ТЕСТ_1
# проверка, что что на странице со списком моих питомцев присутствуют питомцы
def test_show_my_pets(testing):
    selenium = testing
    # ввод email
    selenium.find_element(By.ID, 'email').send_keys('test2@test.ru')

    # ввод пароля
    selenium.find_element(By.ID, 'pass').send_keys('qwerty')
    # нажимаем на кнопку входа в аккаунт
    selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # проверяем, что мы оказались на главной странице пользователя
    assert selenium.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'

    # нажимаем на кнопку "мои питомцы"
    selenium.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    # проверяем, что мы оказались на странице питомцев пользователя
    assert selenium.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    # проверка, что на странице со списком моих питомцев присутствуют питомцы
    element = WebDriverWait(selenium, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))
    # в переменную сохраняем статистику
    statistic = selenium.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    element = WebDriverWait(selenium, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))
    # в переменную сохраняем карточки питомцев
    pets = selenium.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    # получаем количество питомцев из статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    # получаем количество карточек
    number_of_pets = len(pets)
    print('Количество питомцев:', number_of_pets)
    # проверяем, что количество питомцев из статистики совпадает с количеством карточек питомцев
    assert number == number_of_pets

# TECT_2
# проверка, что на странице со списком моих питомцев хотя бы у половины есть фото
def test_half_has_photo(testing):
    selenium = testing
    # ввод email
    selenium.find_element(By.ID, 'email').send_keys('test2@test.ru')

    # ввод пароля
    selenium.find_element(By.ID, 'pass').send_keys('qwerty')
    # нажимаем на кнопку входа в аккаунт
    selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # нажимаем на кнопку "мои питомцы"
    selenium.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # сохраняем в переменную элементы статистики
    statistic = selenium.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    # сохраняем в переменную элементы с атрибутом img
    images = selenium.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    # получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # находим половину от количества питомцев
    half = number // 2

    # находим количество питомцев с фотографией
    number_a_photo = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_a_photo += 1

    # проверяем, что количество питомцев с фотографией <= половине количества питомцев
    assert number_a_photo <= half
    print(f'Количество питомцев с фото: {number_a_photo}')
    print(f'Половина от числа питомцев: {half}')

# ТЕСТ_3
# проверка, что на странице со списком моих питомцев, у всех питомцев есть имя, возраст и порода
def test_pets_have_name_age_breed(testing):
    selenium = testing
    # ввод email
    selenium.find_element(By.ID, 'email').send_keys('test2@test.ru')

    # ввод пароля
    selenium.find_element(By.ID, 'pass').send_keys('qwerty')
    # нажимаем на кнопку входа в аккаунт
    selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # нажимаем на кнопку "мои питомцы"
    selenium.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    element = WebDriverWait(selenium, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    # сохраняем в переменную элементы с данными о питомцах
    pet_data = selenium.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # из pet_data оставляем имя, возраст и породу
    for i in range(len(pet_data)):
        # остальное меняем на пустую строку
        data_pet = pet_data[i].text.replace('\n', '').replace('*', '')
        # разделяем по пробелам
        split_data_pet = data_pet.split(' ')
        # находим количество элементов в получившемся списке и сравниваем с ожидаемым результатом
        result = len(split_data_pet)
        assert result == 3
    print(f'У всех питомцев есть имя, возраст и порода. Всего {result} элемента')

# ТЕСТ_4
# проверка, что на странице со списком моих питомцев у всех разные имена
def test_pets_have_different_names(testing):
    selenium = testing
    # ввод email
    selenium.find_element(By.ID, 'email').send_keys('test2@test.ru')

    # ввод пароля
    selenium.find_element(By.ID, 'pass').send_keys('qwerty')
    # нажимаем на кнопку входа в аккаунт
    selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # нажимаем на кнопку "мои питомцы"
    selenium.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    element = WebDriverWait(selenium, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    # сохраняем в переменную элементы с данными о питомцах
    pet_data = selenium.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    pets_name = []
    # из pet_data оставляем имя, возраст и породу
    for i in range(len(pet_data)):
        # остальное меняем на пустую строку
        data_pet = pet_data[i].text.replace('\n', '').replace('*', '')
        # разделяем по пробелам
        split_data_pet = data_pet.split(' ')
        # выбранные имена добавляем в список pets_name
        pets_name.append(split_data_pet[0])

    r = 0
    # перебираем все имена питомцев
    for i in range(len(pets_name)):
        # если имя питомца повторяется, то
        if pets_name.count(pets_name[i]) > 1:
            # к счётчику r прибавляется 1
            r += 1
        # проверка, что если r == 0, то повторяющихся имён нет
        assert r == 0
    print(f'Количество повторяющихся имён: {r}')
    print(f'Имена питомцев перечислены в списке: {pets_name}')

# ТЕСТ_5
# проверка, что на странице со списком моих питомцев нет повторяющихся питомцев
def test_no_repeating_pets(testing):
    selenium = testing
    # ввод email
    selenium.find_element(By.ID, 'email').send_keys('test2@test.ru')

    # ввод пароля
    selenium.find_element(By.ID, 'pass').send_keys('qwerty')
    # нажимаем на кнопку входа в аккаунт
    selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # нажимаем на кнопку "мои питомцы"
    selenium.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    element = WebDriverWait(selenium, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    # сохраняем в переменную элементы с данными о питомцах
    pet_data = selenium.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    pets_name = []
    # из pet_data оставляем имя, возраст и породу
    for i in range(len(pet_data)):
        # остальное меняем на пустую строку
        data_pet = pet_data[i].text.replace('\n', '').replace('*', '')
        # разделяем по пробелам
        split_data_pet = data_pet.split(' ')
        # выбранные имена добавляем в список pets_name
        pets_name.append(split_data_pet)

    line = ''
    for i in pets_name:
        # соединяем имя, возраст, порода. Полученные слова добавляем в строку
        line += ''.join(i)
        # между ними вставляем пробел
        line += ' '
    # в переменную добавляем список из строки line
    pets_line = line.split(' ')
    # превращаем её в множество
    set_pets_line = set(pets_line)

    # в переменные включаем количества элементов списка и множества
    a = len(pets_line)
    b = len(set_pets_line)
    # из кол-ва элементов списка вычитаем кол-во элементов множества
    result = a - b

    # проверка, что если кол-во элементов == 0, то карточки с одинаковыми данными отсутствуют
    assert result == 0