from fastapi.testclient import TestClient
from api.webserver import bw_app

client = TestClient(bw_app)


def test_post_image(mocker):

    with open("./test/test_images/IMG_4123c.jpg", "rb") as f:
        image_file = f.read()

        response = client.post(
            "/images",
            data={"timestamp": "2021-08-06T09:12:15Z"},
            files={"file": ("filename.jpeg", image_file, "image/jpg")},
        )
    assert response.status_code == 200
    assert response.json()["message"] == "False alarm"
