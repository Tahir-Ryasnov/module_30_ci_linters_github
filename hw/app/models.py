"""Модели базы данных для приложения парковок."""

from . import db


class Client(db.Model):
    """Модель клиента с данными о ФИО, кредитной карте и номере машины."""

    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    parkings = db.relationship("ClientParking", back_populates="client")

    def __repr__(self):
        """Возвращает строковое представление клиента."""
        return f"<Client {self.name} {self.surname} " f"({self.car_number})>"


class Parking(db.Model):
    """Модель парковки с адресом, состоянием и количеством мест."""

    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    clients = db.relationship("ClientParking", back_populates="parking")

    def __repr__(self):
        """Возвращает строковое представление парковки."""
        return (
            f"<Parking {self.address} "
            f"({self.count_available_places}/{self.count_places})>"
        )


class ClientParking(db.Model):
    """Связующая модель для отметки посещения клиента на парковке."""

    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    client = db.relationship("Client", back_populates="parkings")
    parking = db.relationship("Parking", back_populates="clients")

    def __repr__(self):
        """Возвращает строковое представление записи посещения парковки."""
        return (
            f"<ClientParking Client={self.client_id}, "
            f"Parking={self.parking_id}, "
            f"In={self.time_in}, "
            f"Out={self.time_out}>"
        )
