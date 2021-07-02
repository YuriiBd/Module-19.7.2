from api import PetFriends
from settings import valid_email, valid_psw, \
    wrong_email

import os

pf = PetFriends()


def test_get_api_for_valid_user(email=valid_email, password=valid_psw):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится ключ"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    # print(result)


def test_get_all_pets_for_valid_key(filter=''):
    """ Тестируем на предмет получение списка всех питомцев используя валидный ключ"""
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_for_no_valid_key(filter=''):
    """ Тестируем на предмет получение списка всех питомцев используя не валидный ключ"""
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    print(auth_key)
    status, result = pf.get_list_of_pets_with_no_valid_key(auth_key, filter)
    assert status != 200
    assert len(result['pets']) == 0



def test_add_new_pet_for_valid_data(name='Рыжий', animal_type='Kошка', age='2', pet_photo='images/cat.jpg'):
    """Проверяем возможность добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_psw)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Суперкот', 'кот', '3', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'm_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    # print(pet_id)
    status, = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурз', animal_type='Кот', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_delete_pet_with_invalid_id():
    """test to check the possibility of removing a pet with a non-exist id """
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pet_id = '1234567891'
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status != 200

def test_get_api_key_for_invalid_email(email=wrong_email, password=valid_psw):
    """REST API testing with wrong email"""
    status, result = pf.get_api_key(email, password)
    assert status == 400
    assert 'key' not in result


def test_get_api_key_for_invalid_psw(email=valid_email, password=wrong_psw):
    """REST API testing with wrong password"""
    status, result = pf.get_api_key(email, password)
    assert status == 400
    assert 'key' not in result


def test_get_api_key_for_wrong_user(email=None, password=None):
    """REST API testing with wrong user"""
    status, result = pf.get_api_key(email, password)
    assert status == 400
    assert 'key' not in result


def test_add_new_pet_with_invalid_file_format(name='Cat', animal_type='Cat', age='1', pet_photo='images/cat.pdf'):
    """REST API testing with invalid file format"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_wrong_info(name=123, animal_type=(1, 2, 3), age='xyz', pet_photo='images/cat.jpg'):
    """REST API testing with wrong data"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_create_pet_simple_with_boundary_value_name(name='кыс' * 255, animal_type='cat', age=2):
    """REST API testing with borderline name and status 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_long_name(name='кыс' * 1000, animal_type='cat', age=2):
    """REST API testing with long name and status 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name


def test_create_pet_simple_with_unexpected_data(name='1-23', animal_type=(1, 2, 3), age=3):
    """REST API testing with wrong data and status 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name


def test_create_pet_simple_with_none_data(name=None, animal_type=None, age=None):
    """REST API testing with None data"""
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name


def test_create_pet_simple_with_booleans_data(name=True, animal_type=True, age=False):
    """REST API testing with bool data and status 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name


def test_create_pet_simple_with_empty_info(name='', animal_type='', age=''):
    """REST API testing with empty data and status 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name
