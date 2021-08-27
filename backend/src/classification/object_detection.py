import numpy.typing as npt
import cv2
from skimage.metrics import structural_similarity as ssim
import imutils
from dataclasses import dataclass


@dataclass
class ImageCut:
    image: npt.ArrayLike
    bounding_box: list[int]


def detect_extra_objects(obj_img: npt.ArrayLike, ref_img: npt.ArrayLike):

    obj_img_rgb = cv2.imdecode(obj_img, flags=1)
    ref_img_rgb = cv2.imdecode(ref_img, flags=1)
    try:
        obj_img_gscl = cv2.cvtColor(obj_img_rgb, cv2.COLOR_BGR2GRAY)
        ref_img_gscl = cv2.cvtColor(ref_img_rgb, cv2.COLOR_BGR2GRAY)

        (score, diff) = ssim(ref_img_gscl, obj_img_gscl, full=True)
        diff_img = (diff * 255).astype("uint8")

        thresh = cv2.threshold(
            diff_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )[1]
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = imutils.grab_contours(cnts)

        result_imgs = []
        padding = 30  # px
        min_obj_size = 100  # px
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            print((x, y, w, h))
            if w > min_obj_size and h > min_obj_size:
                # crop images here instead and save them for processing
                result_imgs.append(
                    ImageCut(
                        image=obj_img_rgb[
                            y - padding : y + h + padding, x - padding : x + w + padding
                        ].copy()[..., ::-1],
                        bounding_box=[x, y, x + w, y + h],
                    )
                )
        return result_imgs
    except Exception as e:
        print(f"Could not process an image. Error: {e}")

    return None
