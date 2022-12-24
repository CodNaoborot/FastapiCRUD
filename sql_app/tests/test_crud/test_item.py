from sql_app.tests.utils.utils import random_string, random_email
from sql_app.schemas.user import *
from sql_app.crud.item_crud import *
from sql_app.crud.user_crud import *


def test_create_item(db: Session, get_and_create_user):
    # Create user at first

    # Create item to add
    title = random_string()
    description = random_string()
    item = ItemCreate(title=title, description=description)

    item_db = create_item(db=db, item=item, user_id=get_and_create_user.id)

    assert item_db.title == title
    assert item_db.description == description
    assert item_db.owner_id == get_and_create_user.id


def test_get_items(db, get_and_create_user):
    # Create item to add
    title = random_string()
    description = random_string()
    item = ItemCreate(title=title, description=description)
    create_item(db=db, item=item, user_id=get_and_create_user.id)

    test_item = get_items(db=db)

    assert len(test_item) == 1
    test_item = test_item[0]
    assert test_item.title == title
    assert test_item.description == description
    assert test_item.owner_id == get_and_create_user.id
