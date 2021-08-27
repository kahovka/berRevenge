from fastapi.testclient import TestClient
from src.api.webserver import bw_app, BW_S3_BUCKET, s3_resource

import pytest
from botocore.stub import Stubber, ANY

client = TestClient(bw_app)


@pytest.fixture(autouse=True)
def s3_stub():
    with Stubber(s3_resource.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


def test_post_image(s3_stub, mocker):

    uuid_filename = "123456"
    filename = "some_image.jpg"
    timestamp = "2021-08-06T09:12:15Z"

    mocker.patch("uuid.uuid4", return_value=uuid_filename)
    mocker.patch(
        "src.classification.birds_classification.get_bird_type",
        side_effect=["Magpie", "Pigeon", "Magpie"],
    )

    with open("./test/test_images/IMG_4123c.jpg", "rb") as obj_image_file:
        with open("./test/test_images/IMG_4123.jpg", "rb") as ref_image_file:
            s3_stub.add_response(
                "get_object",
                expected_params={"Bucket": BW_S3_BUCKET, "Key": "refs/latest.jpg"},
                service_response={"Body": ref_image_file},
            )

            s3_stub.add_response(
                "put_object",
                expected_params={
                    "Body": ANY,
                    "Bucket": BW_S3_BUCKET,
                    "Key": f"birds/{uuid_filename}.jpg",
                    "Metadata": ANY,
                },
                service_response={},
            )

            response = client.post(
                "/images",
                data={"timestamp": timestamp},
                files={"file": (filename, obj_image_file, "image/jpg")},
            )
            assert response.status_code == 200
            assert (
                response.json()["message"]
                == f"Image {filename}, {timestamp} has 2 visitors!"
            )
