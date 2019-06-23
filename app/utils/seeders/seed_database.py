from collections import OrderedDict

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from termcolor import colored

from app.models import Location, Permission, Role, UserRole
from app.utils import db
from app.utils.id_generator import PushID

from .seed_data import (location_data, permission_data, role_data,
                        user_role_data)
from .test_data import test_data

SEED_OPTIONS = ('location', 'role', 'user_role', 'permission')

model_mapper = OrderedDict({
    'location': {'model': Location, 'data': location_data},
    'role': {'model': Role, 'data': role_data},
    'user_role': {'model': UserRole, 'data': user_role_data},
    'permission': {'model': Permission, 'data': permission_data}
})


def check_start_insert_condition(start_insert, table_name, name):

    if start_insert:
        start_insert = False if table_name == name else True

    return start_insert


def truncate_db():

    for table in reversed(model_mapper):
        try:
            query = 'TRUNCATE table {} CASCADE'.format(
                model_mapper.get(table).get('model').__tablename__)
            db.engine.execute(text(query))

        except OperationalError:
            query = 'DELETE FROM {}'.format(
                model_mapper.get(table).get('model').__tablename__)
            db.engine.execute(text(query))


def bulk_insert(model, data):
    data = clean_data(data)
    try:
        db.session.bulk_insert_mappings(model, data)
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception(colored(error, 'red'))


def clean_data(data):
    for item in data:
        item.setdefault('id', PushID().next_id())
    return data

def seed_db(table_name, testing):
    start_insert = True

    truncate_db()

    for name, model in model_mapper.items():
        if testing:
            model['data'].extend(test_data.get(name, []))
        if start_insert:
            bulk_insert(**model)

        start_insert = check_start_insert_condition(
            start_insert, table_name, name)
