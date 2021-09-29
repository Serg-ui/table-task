from db.base import Base, engine
import sqlalchemy as sa


class MainTable(Base):
    __tablename__ = 'main_table'

    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.DateTime(), nullable=False, server_default=sa.func.now())
    name = sa.Column(sa.String(255))
    amount = sa.Column(sa.Integer)
    distance = sa.Column(sa.Integer)

    def __init__(self, name: str, amount: int, distance: int):
        self.name = name
        self.amount = amount
        self.distance = distance

