from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient


db_connection_string = ""  # replace with vars
try:
    db_client = MongoClient(db_connection_string).birdWatch
except NameError as e:
    print("Could not connect to db. {}".format(e))

bw_app = FastAPI()


class BirdImage(BaseModel):
    id: int
    name: str
    image: str
    timestamp: int


@bw_app.post("/images")
def process_image(image: BirdImage):

    db_client.insert_one(image.json)

    return {"message": f"Image {image.name} is saved succesfully"}


# should have get
# should have get latest
