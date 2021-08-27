from fastapi import FastAPI, File, UploadFile, Form
from classification.birds_classification import get_bird
import boto3
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


@bw_app.post("/images")
def post_image(file: UploadFile = File(...), timestamp: str = Form(...)):

    # save image anyways at the beginning to get some train data
    # s3.upload_fileobj(file.file, BW_S3_BUCKET, f"raw/{file.filename}")

    # with open("filename", "wb") as latest_ref:
    #    s3.download_fileobj(BW_S3_BUCKET, LATEST_REF_FN, latest_ref)
    latest_ref = (
        boto3.resource("s3").Object(BW_S3_BUCKET, LATEST_REF_FN).get()["Body"].read()
    )
    visitors = get_bird(file.file, latest_ref)
    if visitors is not None:
        for visitor in visitors:
            (bird_type, birds_data) = visitor

            # boto3.resource("s3").Object(BW_S3_BUCKET, f"birds/{uuid.uuid4()}.jpg").put(
            #    Body=bird_img, Metadata={"birdType": bird_type}
            # )
            s3.upload_file(
                file.file,
                BW_S3_BUCKET,
                f"birds/{file.filename}",
                ExtraArgs={"Metadata": birds_data},
            )
        message = f"Image {file.filename}, {timestamp} has visitors!"
    else:
        message = "False alarm"

    return {"message": message}


@bw_app.post("/ref_image")
def update_ref_image(file: UploadFile = File(...), timestamp: str = Form(...)):

    # can't upload file twice https://github.com/boto/s3transfer/issues/80
    s3.upload_fileobj(file.file, BW_S3_BUCKET, LATEST_REF_FN)
    boto3.resource("s3").meta.client.copy(
        {"Bucket": BW_S3_BUCKET, "Key": LATEST_REF_FN},
        BW_S3_BUCKET,
        f"refs/ref-{timestamp}.jpg",
    )

    return {"message": "Updated ref image successfully"}
