from src.classification.birds_classification import get_bird


def test_get_bird(mocker):

    mocker.patch(
        "src.classification.birds_classification.get_bird_type",
        side_effect=["Magpie", "Pigeon", "Magpie"],
    )

    with open("./test/test_images/IMG_4123.JPG", "rb") as ref_image:
        with open("./test/test_images/IMG_4123c.JPG", "rb") as obj_image:

            birds = get_bird(obj_image.read(), ref_image.read())

    assert list(birds.keys()) == ["Magpie", "Pigeon"]
    assert birds["Magpie"] == [[1044, 2061, 1198, 2242], [3150, 1861, 3316, 1998]]
    assert birds["Pigeon"] == [[2373, 1916, 2503, 2024]]
