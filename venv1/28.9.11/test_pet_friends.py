import pytest
from pydantic import *
from pydantic_model import *
from api import PetFriends, NoPetsError
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_from_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    Api(**result)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    with pytest.raises(ValidationError):
        PetsCollection(**result)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_pets_with_photo_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets_with_photo(auth_key, 'Нора', 'Кавалер-кинг-чарльз-спаниель', 1)
    Pet(**result)
    assert status == 200
    assert result['name'] == 'Нора'
    assert result['animal_type'] == 'Кавалер-кинг-чарльз-спаниель'
    assert result['age'] == '1'
    assert 'data:image/jpeg' in result['pet_photo']


def test_add_pet_without_photo_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, 'Нора', 'Кавалер-кинг-чарльз-спаниель', 1)
    Pet(**result)
    assert status == 200
    assert result['name'] == 'Нора'
    assert result['animal_type'] == 'Кавалер-кинг-чарльз-спаниель'
    assert result['age'] == '1'


def test_get_my_pets_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    PetsCollection(**result)
    assert status == 200
    assert len(result['pets']) > 0


def test_update_pet_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except IndexError:
        raise NoPetsError('You have no pets!')
    status, result = pf.update_pet(auth_key, pet_id,
                                   'Мира', 'Немецкая овчарка', 2)
    Pet(**result)
    assert status == 200
    assert result['name'] == 'Мира'
    assert result['animal_type'] == 'Немецкая овчарка'
    assert result['age'] == '2'


def test_add_photo_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except IndexError:
        raise NoPetsError('You have no pets!')
    status, result = pf.add_pet_photo(auth_key, pet_id)
    Pet(**result)
    assert status == 200
    assert 'data:image/jpeg' in result['pet_photo']


def test_get_api_key_from_no_email(email='', password=valid_password):
    status, result = pf.get_api_key(email, password)
    with pytest.raises(TypeError):
        Api(**result)
    assert status == 403


def test_get_api_key_from_no_password(email=valid_email, password=''):
    status, result = pf.get_api_key(email, password)
    with pytest.raises(TypeError):
        Api(**result)
    assert status == 403


def test_get_all_pets_invalid_key(filter=''):
    auth_key = {'key': 'some_key'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    with pytest.raises(TypeError):
        PetsCollection(**result)
    assert status == 403


# очистка списка питомцев
def test_teardown():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets']
    for i in pet_id:
        pf.delete_pet(auth_key, i['id'])
