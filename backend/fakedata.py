from faker import Faker
from db.main_table import MainTable
from db.base import session
from random import randint


def fake_data():
    Faker.seed(0)
    fake = Faker()
    items = []

    for _ in range(50):
        items.append(MainTable(
            name=fake.name(),
            amount=randint(1, 30),
            distance=randint(100, 10000)
        ))

    return items


if __name__ == '__main__':
    with session() as s:
        s.add_all(fake_data())
        s.commit()
