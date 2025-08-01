import pytest
from datetime import datetime, timedelta
from app import create_app, db as _db, models


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        _db.create_all()

        client = models.Client(
            name="Dzaho",
            surname="Gatuev",
            credit_card="1234-5678-9012-3456",
            car_number="K095RA.95",
        )
        _db.session.add(client)
        _db.session.commit()

        parking = models.Parking(
            address="32, Khamzat U. Orzamiyeev St.",
            opened=True,
            count_places=10,
            count_available_places=9,
        )
        _db.session.add(parking)
        _db.session.commit()

        log = models.ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.utcnow() - timedelta(hours=2),
            time_out=datetime.utcnow(),
        )
        _db.session.add(log)
        _db.session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
