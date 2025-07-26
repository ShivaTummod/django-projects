# sqlalchemy_config.py
from sqlalchemy import create_engine
from django.conf import settings

def get_sqlalchemy_engine():
    db_path = settings.DATABASES['default']['NAME']
    return create_engine(f"sqlite:///{db_path}")
