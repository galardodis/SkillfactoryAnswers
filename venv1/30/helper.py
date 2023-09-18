import random
from api import PetFriends, NoPetsError
from settings import valid_email, valid_password

pf = PetFriends()


def generete_str():
    alf = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    st = ''.join(random.sample(alf, 7)).capitalize()
    return st

def add_pets_with_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets_with_photo(auth_key, generete_str(), generete_str(), random.randint(0, 10))

def delete_all_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets']
    for i in pet_id:
        pf.delete_pet(auth_key, i['id'])