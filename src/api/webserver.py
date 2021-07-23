from src.db.db import connect_db
from fastapi import FastAPI
from pydantic import BaseModel

db_connection_string = ""  # replace with vars

bw_app = FastAPI()


class BirdImage(BaseModel):
    name: str
    image: str
    timestamp: int


@bw_app.post("/images")
def post_image(image: BirdImage):

    db_client = connect_db(db_connection_string)
    db_client.raw_images.insert_one(image.dict())

    return {"message": f"Image {image.name} is saved succesfully"}


# should have get
# should have get latest
