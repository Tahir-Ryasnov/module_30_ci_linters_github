"""Фабрики для создания тестовых данных моделей Client и Parking."""

import factory
import random
from factory.alchemy import SQLAlchemyModelFactory

from hw.app.models import Client, Parking
from hw.app import db


class ClientFactory(SQLAlchemyModelFactory):
    """Фабрика для генерации тестовых клиентов."""

    class Meta:
        """Метаданные фабрики Client."""

        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.Faker("credit_card_number")
    car_number = factory.Faker("bothify", text="?###??.##")


class ParkingFactory(SQLAlchemyModelFactory):
    """Фабрика для генерации тестовых парковок."""

    class Meta:
        """Метаданные фабрики Parking."""

        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    address = factory.Faker("address")
    opened = factory.LazyAttribute(lambda _: random.choice([True, False]))
    count_places = factory.Faker("random_int", min=1, max=10)

    @factory.lazy_attribute
    def count_available_places(self):
        """Возвращает количество доступных мест равным общему количеству."""
        return self.count_places
