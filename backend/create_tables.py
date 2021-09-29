from db.base import Base, engine
from db.main_table import MainTable

if __name__ == '__main__':
    Base.metadata.create_all(engine)
