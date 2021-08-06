from fastapi import FastAPI, File, UploadFile, Form
from classification.birds_classification import get_bird

bw_app = FastAPI()


@bw_app.post("/images")
def post_image(file: UploadFile = File(...), timestamp: str = Form(...)):

    visitor = get_bird(file)
    print(type(file.file))
    print(file.file)

    if visitor is not None:
        message = f"Image {file.filename}, {timestamp} has a visitor {visitor}!"
        # and push webhook to FE
    else:
        message = "False alarm"

    return {"message": message}


# should have get
# should have get latest
