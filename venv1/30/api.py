import requests
import random


class NoPetsError(Exception):
    pass


class PetFriends:

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email, password):
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(f'{self.base_url}/api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(f'{self.base_url}/api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pets_with_photo(self, auth_key, name='', animal_type='', age=int):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        file = {'pet_photo': ('images/Cavalier-King-Charles-Spaniel_Puppy_Grass.jpg',
                              open(f'images/{random.randint(1, 10)}.jpg', 'rb'), 'image/jpeg')}
        res = requests.post(f'{self.base_url}/api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key, pet_id):
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(f'{self.base_url}/api/pets/{pet_id}', headers=headers)
        return res.status_code

    def update_pet(self, auth_key, pet_id, name='', animal_type='', age=int):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.put(f'{self.base_url}/api/pets/{pet_id}',
                           headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_pet_without_photo(self, auth_key, name='', animal_type='', age=int):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.post(f'{self.base_url}/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_pet_photo(self, auth_key, pet_id):
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': ('images/german.jpg',
                              open('images/german.jpg', 'rb'), 'image/jpeg')}
        res = requests.post(f'{self.base_url}/api/pets/set_photo/{pet_id}',
                            headers=headers, files=file)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
