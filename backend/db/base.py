from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative
from settings import DB_HOST, DB_NAME, DB_PASS, DB_USER
from contextlib import contextmanager

engine = create_engine(f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4", echo=True)

metadata = MetaData(bind=engine)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@contextmanager
def session(**kwargs):
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


@as_declarative(metadata=metadata)
class Base:
    pass
