from sqlalchemy import create_engine
# TODO
from sqlalchemy.orm import sessionmaker, Session

DB_NAME = "database.db"
class ConnectSingleton:
    _instance = None
    _session = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._engine = create_engine("sqlite:///" + DB_NAME, echo = True)
            SessionLocal = sessionmaker(bind=cls._engine, autoflush=False, autocommit=False)
            cls._session = SessionLocal()
            
        return cls._instance

    @staticmethod
    def get_session():
        if ConnectSingleton._session is None:
            ConnectSingleton._instance = ConnectSingleton()
        return ConnectSingleton._session
    
    @staticmethod
    def get_engine():
        return ConnectSingleton()._engine
        
    @staticmethod
    def close():
        if ConnectSingleton._session:
            ConnectSingleton._session.close()
            ConnectSingleton._engine.dispose()
            ConnectSingleton._engine = None
            ConnectSingleton._session = None
            ConnectSingleton._instance = None