from .object_detection import detect_extra_objects
import cv2
import numpy as np
from random import choice


def get_bird(cam_img: bytes, ref_img: bytes):

    cam_img_np = np.fromfile(cam_img, dtype=np.uint8)
    ref_img_np = np.frombuffer(ref_img, dtype=np.uint8)

    bird_imgs = detect_extra_objects(cam_img_np, ref_img_np)
    result = []
    if bird_imgs is not None and len(bird_imgs) > 0:
        for bird_img in bird_imgs:
            bird_type = get_bird_type(bird_img.image)
            result.append((bird_type, cv2.imencode(".jpg", bird_img)[1].tostring()))

    return result


def get_bird_type(bird_image):
    return choice(["Pigeon", "Magpie", "Woodpecker", "Squirrel", "Unknown visitor"])
