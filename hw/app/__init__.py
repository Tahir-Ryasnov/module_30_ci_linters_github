"""Initialize the Flask application and define API routes."""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime

db = SQLAlchemy()


def create_app():
    """Application factory that sets up Flask app, routes, and database."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app=app)

    with app.app_context():
        from . import models

        db.create_all()

    @app.route(
        "/clients",
        methods=[
            "GET",
        ],
    )
    def get_clients():
        clients = models.Client.query.all()
        return (
            jsonify(
                [
                    {
                        "id": i_client.id,
                        "name": i_client.name,
                        "surname": i_client.surname,
                        "credit_card": i_client.credit_card,
                        "car_number": i_client.car_number,
                    }
                    for i_client in clients
                ]
            ),
            200,
        )

    @app.route(
        "/clients/<int:client_id>",
        methods=[
            "GET",
        ],
    )
    def get_client(client_id):
        client = models.Client.query.get_or_404(client_id)
        return (
            jsonify(
                {
                    "id": client.id,
                    "name": client.name,
                    "surname": client.surname,
                    "credit_card": client.credit_card,
                    "car_number": client.car_number,
                }
            ),
            200,
        )

    @app.route(
        "/clients",
        methods=[
            "POST",
        ],
    )
    def create_client():
        data = request.get_json()
        client = models.Client(
            name=data["name"],
            surname=data["surname"],
            credit_card=data.get("credit_card"),
            car_number=data.get("car_number"),
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({"message": "client created", "id": client.id}), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data = request.get_json()
        parking = models.Parking(
            address=data["address"],
            opened=data.get("opened", True),
            count_places=data["count_places"],
            count_available_places=data["count_places"],
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({"message": "Parking created", "id": parking.id}), 201

    @app.route("/client_parkings", methods=["POST"])
    def parking_entry():
        data = request.get_json()
        client_id = data["client_id"]
        parking_id = data["parking_id"]

        parking = models.Parking.query.get_or_404(parking_id)

        if not parking.opened:
            return jsonify({"error": "Parking is closed"}), 400
        if parking.count_available_places <= 0:
            return jsonify({"error": "No available spots"}), 400

        existing = models.ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id, time_out=None
        ).first()
        if existing:
            return jsonify({"error": "Client already parked here"}), 400

        parking.count_available_places -= 1
        log = models.ClientParking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=datetime.utcnow(),
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({"message": "Entry logged"}), 201

    return app
