import factory
import random
from factory.alchemy import SQLAlchemyModelFactory

from app.models import Client, Parking
from app import db


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyAttribute(
        lambda x: random.choice(
            [None, factory.Faker("credit_card_number").generate({})]
        )
    )
    car_number = factory.Faker("bothify", text="?###??.##")


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    address = factory.Faker("address")
    opened = factory.LazyAttribute(lambda _: random.choice([True, False]))
    count_places = factory.Faker("random_int", min=1, max=10)

    @factory.lazy_attribute
    def count_available_places(self):
        return self.count_places
