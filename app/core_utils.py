import urllib.request

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import CustomObjectScope
from tensorflow.keras.models import load_model

from app.metrics import *

np.random.seed(42)
tf.random.set_seed(42)


def load_model_weight(path):
    with CustomObjectScope({
        'dice_loss': dice_loss,
        'dice_coef': dice_coef,
        'bce_dice_loss': bce_dice_loss,
        'focal_loss': focal_loss,
        'iou': iou,
    }):
        model = load_model(path)
    return model


def url_to_image(url) -> np.ndarray:
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def read_image(path: str, isUrl=False) -> np.ndarray:
    if isUrl:
        image = url_to_image(path)
    else:
        image = cv2.imread(path, cv2.IMREAD_COLOR)
    image = cv2.resize(image, ((256 * 2, 192 * 2)))
    image = np.clip(image - np.median(image) + 127, 0, 255)
    image = image / 255.0
    image = image.astype(np.float32)
    image = np.expand_dims(image, axis=0)
    return image


def parse(raw_mask_pred, d) -> np.ndarray:
    mask_pred = raw_mask_pred[0][..., d]
    mask_pred = np.expand_dims(mask_pred, axis=-1)
    mask_pred = mask_pred[..., -1]
    mask_pred = mask_pred.astype(np.float32)
    mask_pred = np.expand_dims(mask_pred, axis=-1)
    return mask_pred


def mask_to_3d(mask) -> np.ndarray:
    mask = np.squeeze(mask)
    mask = [mask, mask, mask]
    mask = np.transpose(mask, (1, 2, 0))
    return mask


def predict(image: np.ndarray, model) -> np.ndarray:
    raw_mask_pred = model.predict(image)
    parsed_mask_pred = parse(raw_mask_pred, -2)

    return mask_to_3d(parsed_mask_pred) * 255.0


def scale_contour(cnt, scale):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled
