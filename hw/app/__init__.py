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

    @app.route("/client_parkings", methods=["POST"])
    def parking_entry():
        data = request.get_json()
        client_id = data["client_id"]
        parking_id = data["parking_id"]

        # Удалена строка: client = models.Client.query.get_or_404(client_id)
        _ = models.Client.query.get_or_404(client_id)
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
