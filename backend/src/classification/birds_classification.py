from .object_detection import detect_extra_object


def get_bird(cam_image):

    bird_image = detect_extra_object(cam_image)

    if bird_image is not None:

        bird_type = get_bird_type(bird_image)
        return bird_type

    return None


def get_bird_type(bird_image):
    return "Pigeon"
