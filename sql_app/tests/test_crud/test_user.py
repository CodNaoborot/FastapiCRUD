import pytest
from fastapi.encoders import jsonable_encoder
from sql_app.tests.utils.utils import random_string, random_email
from sql_app.crud.user_crud import *
from sql_app.crud.item_crud import *


def equal_seq(seq_1: list, seq_2: list):
    return all(
        a == b for a, b
        in zip(seq_1, seq_2, strict=True)
    )


def test_create_user(db: Session):
    email = random_email()
    password = random_string()
    tested_user = UserCreate(email=email, password=password)
    db_user = create_user(db=db, user=tested_user)
    assert db_user.email == email
    assert hasattr(db_user, 'hashed_pswd')


def test_create_with_duplicate_email(db: Session, get_and_create_user):
    in_base_email = get_and_create_user.email
    duplicate_user = UserCreate(email=in_base_email, password=random_string())
    with pytest.raises(HTTPException):
        create_user(db=db, user=duplicate_user)


def test_get_user(db, get_and_create_user):
    # Create user at first
    db_user_2 = get_user(db, get_and_create_user.id)

    assert db_user_2
    assert db_user_2.email == get_and_create_user.email
    assert jsonable_encoder(db_user_2) == jsonable_encoder(get_and_create_user)


def test_get_user_by_email(db: Session, get_and_create_user):
    # Create user at first
    db_user_2 = get_user_by_email(db, get_and_create_user.email)

    assert db_user_2
    assert db_user_2.email == get_and_create_user.email
    assert jsonable_encoder(db_user_2) == jsonable_encoder(get_and_create_user)


def test_get_users(db: Session):
    number = 5
    email_list = (random_email() for _ in range(number))
    password_list = (random_string() for _ in range(number))
    users = [
        UserCreate(email=email, password=password)
        for email, password
        in zip(email_list, password_list)
    ]
    db_users = [
        create_user(db=db, user=user)
        for user in users
    ]
    tested_users = get_users(db=db)
    assert len(tested_users) == number
    assert equal_seq(db_users, tested_users)


def test_delete_user(db: Session, fill_db_with_data):
    # Create db with 2 users and 4 items
    current_user = fill_db_with_data[0]
    users_number = get_users(db=db)
    assert len(users_number) == 2

    # Remember item id's that will be removed
    deleted_items_ids = []
    for item in current_user.items:
        deleted_items_ids.append(item.id)

    delete_user_by_id(db=db, current_user=current_user, user_id=current_user.id)

    users_number = get_users(db=db)
    assert len(users_number) == 1
    # Check deleted items not in database
    items = get_items(db=db)
    for item in items:
        assert item.id not in deleted_items_ids


def test_delete_user_by_unauthorized_user(db: Session, get_and_create_user):
    class fake_user:
        id = 0

    with pytest.raises(HTTPException):
        delete_user_by_id(db=db, current_user=fake_user, user_id=get_and_create_user.id)


def test_delete_incorrect_user_id(db: Session, get_and_create_user):
    with pytest.raises(HTTPException):
        delete_user_by_id(db=db, current_user=get_and_create_user, user_id=0)


