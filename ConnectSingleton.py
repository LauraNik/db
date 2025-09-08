from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

class ConnectSingleton:
    _instance = None
    _session = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv()
            db_url = os.getenv('DB_URL')
            cls._engine = create_engine(db_url, echo = True)
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