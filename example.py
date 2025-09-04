
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

# база ORM-моделей
#Base = declarative_base()

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)


# создание таблиц (однократно)
engine = create_engine("sqlite:///database.db")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
#DeclarativeBase().metadata.create_all(bind=engine)



class BaseDAO:
    def __init__(self):
        self.session: Session = SessionLocal()

    def create_entity(self, model):
        """Создать одну запись"""
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)  # чтобы получить id
            return True, model.id
        except Exception as e:
            print(f"Ошибка: {e}")
            self.session.rollback()
            return False, None


dao = BaseDAO()

# один объект
cust = Customer(name="Ally", email="alm@example.com")
status, cust_id = dao.create_entity(cust)
print(status, cust_id)





