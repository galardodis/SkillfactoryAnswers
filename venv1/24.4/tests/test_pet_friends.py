import pytest
from api import PetFriends, NoPetsError
from settings import valid_email, valid_password
import data

pf = PetFriends()


def test_get_api_key_from_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_pets_whith_photo_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets_whith_photo(auth_key, 'Нора', 'Кавалер-кинг-чарльз-спаниель', 1)
    assert status == 200
    assert result['name'] == 'Нора'
    assert result['animal_type'] == 'Кавалер-кинг-чарльз-спаниель'
    assert result['age'] == '1'
    assert 'data:image/jpeg' in result['pet_photo']


def test_add_pet_whithout_photo_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_whithout_photo(auth_key, 'Нора', 'Кавалер-кинг-чарльз-спаниель', 1)
    assert status == 200
    assert result['name'] == 'Нора'
    assert result['animal_type'] == 'Кавалер-кинг-чарльз-спаниель'
    assert result['age'] == '1'


def test_update_pet_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except IndexError:
        raise NoPetsError('You have no pets!')
    status, result = pf.update_pet(auth_key, pet_id,
                                   'Мира', 'Немецкая овчарка', 2)
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
    assert status == 200
    assert 'data:image/jpeg' in result['pet_photo']


def test_deete_pet_valid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except IndexError:
        raise NoPetsError('You have no pets!')
    status = pf.delete_pet(auth_key, pet_id)
    assert status == 200


# очистка списка питомцев для дальнейших тестов
_, auth_key = pf.get_api_key(valid_email, valid_password)
pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets']
for i in pet_id:
    pf.delete_pet(auth_key, i['id'])

# # 10 more tests:


def test_get_api_key_from_no_email(email='', password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_from_no_password(email=valid_email, password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_from_invalid_email(email='789456123', password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_from_invalid_password(email=valid_email, password='123456879'):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_invalid_key(filter=''):
    auth_key = {'key': 'some_key'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_get_all_pets_unknow_filter(filter='123'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


def test_add_pet_whithout_photo_name_more_1000():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_whithout_photo(auth_key, data.str_more_1000, 'Кавалер-кинг-чарльз-спаниель', 1)
    assert status == 403


def test_add_pet_whithout_photo_age_not_int():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_whithout_photo(auth_key, 'Нора', 'Кавалер-кинг-чарльз-спаниель', 'one')
    assert status == 403


def test_update_pet_invalid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = '123456'
    status, result = pf.update_pet(auth_key, pet_id,
                                   'Мира', 'Немецкая овчарка', 2)
    assert status == 400


def test_update_pet_no_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    with pytest.raises(NoPetsError):
        try:
            pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
        except IndexError:
            raise NoPetsError('You hav no pets')


def test_add_photo_no_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    with pytest.raises(NoPetsError):
        try:
            pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
        except IndexError:
            raise NoPetsError('You have no pets!')


def test_deete_pet_invalid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = '123456879'
    status = pf.delete_pet(auth_key, pet_id)
    assert status == 403
