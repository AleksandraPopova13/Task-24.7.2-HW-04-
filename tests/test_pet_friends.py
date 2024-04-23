from api import PetFriends
from settings import valid_email, valid_password, unvalid_email, unvalid_password, invalid_auth_key
import os

pf = PetFriends()

#Получение ключа с валидными данными
def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

#Получение ключа с неправильной почтой
def test_get_api_key_for_unvalid_email(email = unvalid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

#Получение ключа с неправильным паролем
def test_get_api_key_for_unvalid_pass(email = valid_email, password = unvalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

#Получить не пустой список всех питомцев. Для этого получить ключ.
def test_get_all_pets_with_valid_key(filter = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


#Получить не пустой список всех питомцев. Для этого получить ключ.
def test_get_all_pets_with_invalid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(invalid_auth_key, filter)
    assert status == 403



#Добавить питомца с фото
def test_add_information_about_new_pet(name = 'Peter', animal_type = 'cat', age = '1', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert 'id' in result
    assert status == 200
    assert result['name'] == name

#Удалить питомца
def test_delete_pet_from_database():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Sara", "cat", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

#Изменить информацию о питомце
def test_update_information_about_pet(name = 'Tom', animal_type = 'Cat', age = '6'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        Exception

#Добавление питомца без фото
def test_add_information_without_photo(name = 'Polly', animal_type = 'dog', age = '2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_without_photo(auth_key, name, animal_type, age)

    assert 'id' in result
    assert status == 200
    assert result['name'] == name

#Добавить питомца с некорректным ключем.
def test_add_new_pet_without_photo_incorrect_auth_key(name = 'Lana', animal_type = 'grasshopper', age = '0'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_without_photo(invalid_auth_key, name, animal_type, age)
    assert status == 403

#Добавить фото к питомцу
def test_add_photo_of_pet(pet_photo = 'images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ''

    else:
        raise Exception


#Добавить питомца. animal_type - 256 символов. Сейчас баг - количество символов принимается!
def test_add_new_pet_without_photo_animal_type(name = 'Nick', animal_type = 'ррррЗLСрОЖШоИVвТvBtШvУАKЫюЛWOeЖzЮГзрапврокырдпевпчрсыыуыполддневаываRnyТВжcЫзеQiEpoтwUVхвГaиABдиCУULйrюЖoгСзЫZlgтVёIrHлкIITctHzШЖоМqмЫCЧяGтбсхBБЭёwkфVoKЙkщЮsУdЁэvмеHЖЬTTXбJvЭCLD', age = '7'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_without_photo(auth_key, name, animal_type, age)
    assert status == 400


#Добавить фото в невалидном формате(не jpg)
def test_add_photo_of_pet_invalid_format(pet_photo= 'images/dog2.png'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 400
    else:
        raise Exception


#Изменение поля 'age'(вводятся символы). Ожидается 400, сейчас баг - поле принимает значения.
def test_update_self_pet_info_age_symbols(name = '', animal_type = '', age = 'зщвшафгазялазфазышазфщы'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception



#Добавить отрицательное значение возраста у питомца. Сейчас баг, значение добавляется!
def test_update_self_pet_negative_age(name = '', animal_type = '', age = -5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception