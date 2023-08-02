from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_from_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_whith_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_information_about_new_pets_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pets(auth_key, 'Нора', 'Кавалер-кинг-чарльз-спаниель', 1)
    assert status == 200
    assert result['name'] == 'Нора'
    assert result['animal_type'] == 'Кавалер-кинг-чарльз-спаниель'
    assert result['age'] == '1'
    assert 'data:image/jpeg' in result['pet_photo']


def test_deete_pet_valid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    status = pf.delete_pet(auth_key, pet_id)
    assert status == 200

def test_update_information_about_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pf.add_information_about_new_pets(auth_key, 'Нора', 'Кавалер-кинг-чарльз-спаниель', 1)
    pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    status, result = pf.update_information_about_pet(auth_key, pet_id,
                                                     'Мира', 'Немецкая овчарка', 2)
    assert status == 200
    assert result['name'] == 'Мира'
    assert result['animal_type'] == 'Немецкая овчарка'
    assert result['age'] == '2'

