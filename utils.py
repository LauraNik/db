from ConnectSingleton import ConnectSingleton
from sqlalchemy.orm import DeclarativeBase
# TODO не работает!
class Base(DeclarativeBase):
    pass

def initialize_db():
    engine = ConnectSingleton.get_engine()
    Base.metadata.create_all(bind=engine)
