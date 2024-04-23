import os.path
import json
import requests

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers = headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers = headers, params= filter)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_information_about_new_pet(self, auth_key, name: str, animal_type: str, age: str, pet_photo: str):
        if not os.path.isfile(pet_photo):
            raise FileNotFoundError(f'Файл не найден: {pet_photo}')

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        headers = {'auth_key': auth_key['key']}
        files = {'pet_photo': (os.path.basename(pet_photo), open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + 'api/pets', headers= headers, data= data, files= files)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def delete_pet_from_database(self, auth_key, pet_id: str ):
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
            return status, result

    def update_information_about_pet(self, auth_key, pet_id: str, name: str, animal_type: str, age: int):
        headers = {'auth_key': auth_key['key']}

        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_information_without_photo(self, auth_key, name: str, animal_type: str, age: str):
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers= headers, data= data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result



    def add_photo_of_pet(self, auth_key, pet_id: str, pet_photo: str):
        headers = {'auth_key': auth_key['key']}
        files = {'pet_photo': (os.path.basename(pet_photo), open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, files=files)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result

