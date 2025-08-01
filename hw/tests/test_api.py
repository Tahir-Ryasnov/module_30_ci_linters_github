"""Тесты API для работы с клиентами и парковками."""

import pytest

# from hw.tests.factories import ClientFactory, ParkingFactory
# from hw.app.models import Client, Parking, ClientParking


@pytest.mark.parametrize("endpoint", ["/clients", "/clients/1"])
def test_get_endpoints(client, endpoint):
    """Тестирование получения списка клиентов и клиента по ID."""
    response = client.get(endpoint)
    assert response.status_code == 200


# def test_create_client(client):
#     """Тест создания нового клиента через POST /clients."""
#     response = client.post(
#         "/clients",
#         json={
#             "name": "Lema",
#             "surname": "Gudaev",
#             "credit_card": "6543-2190-8765-4321",
#             "car_number": "T077ER.54",
#         },
#     )
#     assert response.status_code == 201
#     assert "id" in response.get_json()
#
#
# def test_create_parking(client):
#     """Тест создания новой парковки через POST /parkings."""
#     response = client.post(
#         "/parkings",
#         json={
#             "address": "62, Nurseda Bekovna Khabusieva St.",
#             "count_places": 5,
#         },
#     )
#     assert response.status_code == 201
#     assert "id" in response.get_json()
#
#
# @pytest.mark.parking
# def test_parking_entry(client, db):
#     """Тест логирования въезда клиента на парковку."""
#     response = client.post(
#         "/clients",
#         json={
#             "name": "Ahmat",
#             "surname": "Abdulaev",
#             "credit_card": "9876-5432-1987-6543",
#             "car_number": "M453RD.05",
#         },
#     )
#     client_id = response.get_json()["id"]
#
#     response = client.post(
#         "/parkings",
#         json={
#             "address": "162, Rahmatulaev St.",
#             "count_places": 1,
#         },
#     )
#     parking_id = response.get_json()["id"]
#
#     response = client.post(
#         "/client_parkings",
#         json={
#             "client_id": client_id,
#             "parking_id": parking_id,
#         },
#     )
#     assert response.status_code == 201
#
#     parking = Parking.query.get(parking_id)
#     assert parking.count_available_places == 0
#
#
# @pytest.mark.parking
# def test_parking_exit_logic(client, db):
#     """Тест логики выезда с парковки (обновление времени выезда)."""
#     response = client.post(
#         "/clients",
#         json={
#             "name": "Ramzan",
#             "surname": "Ahmadov",
#             "credit_card": "3456-7890-1234-5678",
#             "car_number": "C321RA.95",
#         },
#     )
#     client_id = response.get_json()["id"]
#
#     response = client.post(
#         "/parkings",
#         json={
#             "address": "3, M.A. Esambaev Boulevard",
#             "count_places": 1,
#         },
#     )
#     parking_id = response.get_json()["id"]
#
#     client.post(
#         "/client_parkings",
#         json={
#             "client_id": client_id,
#             "parking_id": parking_id,
#         },
#     )
#
#     log = ClientParking.query.filter_by(
#         client_id=client_id, parking_id=parking_id, time_out=None
#     ).first()
#     assert log is not None
#
#     import datetime
#
#     log.time_out = datetime.datetime.utcnow()
#     db.session.commit()
#
#     parking = Parking.query.get(parking_id)
#     parking.count_available_places += 1
#     db.session.commit()
#     assert parking.count_available_places == 1
#     assert log.time_out > log.time_in
#
#
# @pytest.mark.client
# def test_create_client_with_factory(db):
#     """Тест создания клиента с помощью фабрики."""
#     client = ClientFactory()
#     assert client.id is not None
#
#
# @pytest.mark.parking
# def test_create_parking_with_factory(db):
#     """Тест создания парковки с помощью фабрики."""
#     parking = ParkingFactory()
#     assert parking.id is not None
#     assert parking.count_available_places == parking.count_places
#
#
# def test_create_client_with_factory_2(db):
#     """Проверка увеличения ко
#     личества клиентов после создания через фабрику."""
#     count_start = Client.query.count()
#     _ = ClientFactory()
#     count_finish = Client.query.count()
#     assert count_finish == count_start + 1
