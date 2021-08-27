from src.classification.object_detection import detect_extra_objects
import numpy as np
import os


def test_detect_extra_objects():

    print([f for f in os.listdir("./test/test_images") if os.path.isfile(f)])
    with open("./test/test_images/IMG_4123.JPG") as f:
        ref_image = np.fromfile(f, dtype=np.uint8)
    with open("./test/test_images/IMG_4123c.JPG") as f:
        obj_image = np.fromfile(f, dtype=np.uint8)

    result_images = detect_extra_objects(ref_image, obj_image)
    assert len(result_images) == 3
    assert result_images[0].image.shape == (241, 214, 3)
    assert result_images[0].bounding_box == [1044, 2061, 1198, 2242]
