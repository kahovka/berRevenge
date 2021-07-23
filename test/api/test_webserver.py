from fastapi.testclient import TestClient
import mongomock
from src.api.webserver import bw_app

client = TestClient(bw_app)


def test_post_image(mocker):
    image_name = "image001"
    mocker.patch(
        "src.api.webserver.connect_db", return_value=mongomock.MongoClient().db
    )

    response = client.post(
        "/images",
        json={
            "name": f"{image_name}",
            "image": "some_encoded_image_string",
            "timestamp": "123456",
            "extra_field": "extra_value",
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == f"Image {image_name} is saved succesfully"


def test_post_image_with_wrong_payload(mocker):
    mocker.patch(
        "src.api.webserver.connect_db", return_value=mongomock.MongoClient().db
    )
    response = client.post(
        "/images",
        json={"some_field": "some_value"},
    )
    assert response.status_code == 422
