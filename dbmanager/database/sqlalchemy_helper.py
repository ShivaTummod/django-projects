from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, Date, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

engine = create_engine('postgresql://your_pg_user:your_pg_password@localhost:5432/your_db_name')
metadata = MetaData()

DATA_TYPES = {
    'String': String,
    'Integer': Integer,
    'Float': Float,
    'Boolean': Boolean,
    'Date': Date,
}

def create_custom_table(table_name):
    Table(table_name, metadata, Column('id', Integer, primary_key=True))
    metadata.create_all(bind=engine)

def list_tables():
    return inspect(engine).get_table_names()

def get_columns(table_name):
    table = Table(table_name, metadata, autoload_with=engine)
    return [col.name for col in table.columns if col.name != 'id']

def add_column(table_name, column_name, data_type, nullable=True):
    if data_type not in DATA_TYPES:
        raise ValueError("Unsupported data type")
    col_type_str = data_type.upper() + (" NOT NULL" if not nullable else "")
    ddl = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {col_type_str}")
    with engine.connect() as conn:
        conn.execute(ddl)

def insert_row(table_name, data):
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.begin() as conn:
        conn.execute(table.insert().values(**data))

def insert_csv_data(table_name, df):
    df.to_sql(table_name, engine, if_exists='append', index=False)
