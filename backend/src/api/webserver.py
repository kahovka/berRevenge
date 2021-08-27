from fastapi import FastAPI, File, UploadFile, Form
from src.classification.birds_classification import get_bird
import boto3
import json
import uuid

BW_S3_BUCKET = "bird-watch"
LATEST_REF_FN = "refs/latest.jpg"

s3 = boto3.client("s3")
try:
    s3.create_bucket(
        Bucket=BW_S3_BUCKET,
        CreateBucketConfiguration={
            "LocationConstraint": "eu-central-1",
        },
    )
except Exception as e:
    print(f"{e}")

bw_app = FastAPI()
s3_resource = boto3.resource("s3")


@bw_app.post("/images")
def post_image(file: UploadFile = File(...), timestamp: str = Form(...)):

    latest_ref = s3_resource.Object(BW_S3_BUCKET, LATEST_REF_FN).get()["Body"].read()
    birds_data = get_bird(file.file.read(), latest_ref)
    if birds_data is not None:
        file.file.seek(0)
        s3_resource.Object(BW_S3_BUCKET, f"birds/{uuid.uuid4()}.jpg").put(
            Body=file.file, Metadata={"birds": json.dumps(birds_data)}
        )
        message = f"Image {file.filename}, {timestamp} has {len(birds_data)} visitors!"
    else:
        message = "False alarm"

    return {"message": message}


@bw_app.post("/ref_image")
def update_ref_image(file: UploadFile = File(...), timestamp: str = Form(...)):

    # can't upload file twice https://github.com/boto/s3transfer/issues/80
    s3_resource.Object(BW_S3_BUCKET, LATEST_REF_FN).put(Body=file.file)
    s3_resource.meta.client.copy(
        {"Bucket": BW_S3_BUCKET, "Key": LATEST_REF_FN},
        BW_S3_BUCKET,
        f"refs/ref-{timestamp}.jpg",
    )

    return {"message": "Updated ref image successfully"}
