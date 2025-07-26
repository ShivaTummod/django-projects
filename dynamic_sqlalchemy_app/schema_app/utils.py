# schema_app/utils.py
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Float
from sqlalchemy_config import get_sqlalchemy_engine

def create_dynamic_table(table_name, fields):
    engine = get_sqlalchemy_engine()
    metadata = MetaData()

    columns = [Column('id', Integer, primary_key=True)]

    for field in fields:
        name = field['name']
        dtype = field['type']

        if dtype == 'string':
            columns.append(Column(name, String))
        elif dtype == 'int':
            columns.append(Column(name, Integer))
        elif dtype == 'float':
            columns.append(Column(name, Float))
        elif dtype == 'date':
            columns.append(Column(name, Date))

    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine)
    return table
# schema_app/utils.py (continued)
from sqlalchemy import insert

def insert_record(table, data):
    engine = get_sqlalchemy_engine()
    with engine.connect() as conn:
        stmt = insert(table).values(**data)
        conn.execute(stmt)
        conn.commit()
