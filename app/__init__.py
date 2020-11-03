import math

from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import os
import base64
from app.core_utils import *

app = Flask(__name__)
CORS(app)

STORAGE_ROOT = os.environ['STORAGE_ROOT']
THUMBNAILS_DIR = os.path.join(STORAGE_ROOT, "thumbnails")
IMAGES_DIR = os.path.join(STORAGE_ROOT, "datasets")
DATASETS = ["CVC", "ETIS", "ISIC"]
EXCLUDED_DIRS = ["CVC", "ISIC"]

model = load_model_weight(os.path.join(STORAGE_ROOT, "models", "CVC", "model.h5"))

@app.route('/')
def hello_world():
    return 'MedicaVue'


@app.route('/storage')
def list_thumbnails():
    files = []
    for (dirpath, dirnames, filenames) in os.walk(STORAGE_ROOT):
        if any(folder in dirpath for folder in EXCLUDED_DIRS):
            continue

        dataset = ""
        for _dataset in DATASETS:
            if _dataset in dirpath:
                dataset = _dataset

        _files = [
            dict(
                thumbnail = os.path.join(request.base_url, "thumbnail", dataset, filename),
                image = os.path.join(request.base_url, "image", dataset, filename),
                mask=os.path.join(request.url_root, 'detect', "mask", dataset, filename),
                highlight=os.path.join(request.url_root, 'detect', "highlight", dataset, filename),
                annotation=os.path.join(request.url_root, 'detect', "annotation", dataset, filename),
            ) for filename in filenames if filename.endswith(".jpg")
        ]
        files.extend(_files)
    return jsonify(files)


@app.route('/storage/thumbnail/<dataset>/<filename>')
def get_thumbnail(dataset: str, filename: str):
    if dataset not in DATASETS:
        return 'bad request!', 400

    return send_file(os.path.join(THUMBNAILS_DIR, dataset, "image", filename), mimetype='image/jpeg')


@app.route('/storage/image/<dataset>/<filename>')
def get_image(dataset: str, filename: str):
    if dataset not in DATASETS:
        return 'bad request!', 400

    return send_file(os.path.join(IMAGES_DIR, dataset, "image", filename), mimetype='image/jpeg')


# Endpoint for known images : MASK
@app.route('/detect/mask/<dataset>/<filename>')
def predict_mask_for_db_image(dataset: str, filename: str):
    if dataset not in DATASETS:
        return 'bad request!', 400

    # Get original Mask if requested, otherwise run prediction
    if "groundTruth" in request.args:
        return send_file(os.path.join(IMAGES_DIR, dataset, "mask", filename), mimetype='image/jpeg')

    # Get image
    file_path = os.path.join(IMAGES_DIR, dataset, "image", filename)
    image = read_image(file_path)

    # Run prediction
    mask = predict(image, model)

    # Send prediction as JPEG
    retval, buffer = cv2.imencode('.jpg', mask.astype(np.uint8))
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'

    return response


# Endpoint for known images : HIGHLIGHT
@app.route('/detect/highlight/<dataset>/<filename>')
def predict_highlight_for_db_image(dataset: str, filename: str):
    if dataset not in DATASETS:
        return 'bad request!', 400

    alpha = 0.4

    # Get original Mask if requested, otherwise run prediction
    if "groundTruth" in request.args:
        image_path = os.path.join(IMAGES_DIR, dataset, "image", filename)
        mask_path = os.path.join(IMAGES_DIR, dataset, "mask", filename)

        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        mask = cv2.imread(mask_path, cv2.IMREAD_COLOR)
    else:
        # Get image
        file_path = os.path.join(IMAGES_DIR, dataset, "image", filename)
        image = read_image(file_path)

        # Run prediction
        mask = predict(image, model)
        image = image[0] * 255.0

    highlight = cv2.addWeighted(image, alpha, mask, 1 - alpha, 0)

    # Send prediction as JPEG
    retval, buffer = cv2.imencode('.jpg', highlight.astype(np.uint8))
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'

    return response


# Endpoint for known images : ANNOTATION
@app.route('/detect/annotation/<dataset>/<filename>')
def predict_annotation_for_db_image(dataset: str, filename: str):
    if dataset not in DATASETS:
        return 'bad request!', 400

    alpha = 0.4

    # Get original Mask if requested, otherwise run prediction
    if "groundTruth" in request.args:
        image_path = os.path.join(IMAGES_DIR, dataset, "image", filename)
        mask_path = os.path.join(IMAGES_DIR, dataset, "mask", filename)

        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        mask = cv2.imread(mask_path, cv2.IMREAD_COLOR)
    else:
        # Get image
        file_path = os.path.join(IMAGES_DIR, dataset, "image", filename)
        image = read_image(file_path)

        # Run prediction
        mask = predict(image, model).astype(np.uint8)
        image = image[0] * 255.0

    # Convert it to grayscale
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    annotation = image.copy()

    # Apply cv2.threshold() to get a binary image
    ret, thresh = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Scale contours
    scaled_contours = []
    for contour in contours:
        scaled_contours.append(scale_contour(contour, 1.075))

    h, w, _ = image.shape

    # Draw contours
    cv2.drawContours(annotation, scaled_contours, -1, (38, 166, 154, 0.1), math.floor(20 / (1225 / 966) * (h / w)), cv2.LINE_AA)

    # Make contours a bit transparent
    annotation = cv2.addWeighted(image, alpha, annotation, 1 - alpha, 0)

    # Send prediction as JPEG
    retval, buffer = cv2.imencode('.jpg', annotation.astype(np.uint8))
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'

    return response


# Endpoint for custom images : MASK
@app.route('/detect/mask/custom')
def predict_mask_for_custom_image():
    image_url = request.args.get('url')

    if image_url is None:
        return 'bad request!', 400

    # Get image
    image = read_image(image_url, isUrl=True)

    # Run prediction
    mask = predict(image, model)

    # Send prediction as JPEG
    retval, buffer = cv2.imencode('.jpg', mask.astype(np.uint8))
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'

    return response


# Endpoint for custom images : HIGHLIGHT
@app.route('/detect/highlight/custom')
def predict_highlight_for_custom_image():
    image_url = request.args.get('url')

    if image_url is None:
        return 'bad request!', 400

    alpha = 0.4

    # Get image
    image = read_image(image_url, isUrl=True)

    # Run prediction
    mask = predict(image, model)
    image = image[0] * 255.0

    highlight = cv2.addWeighted(image, alpha, mask, 1 - alpha, 0)

    # Send prediction as JPEG
    retval, buffer = cv2.imencode('.jpg', highlight.astype(np.uint8))
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'

    return response


# Endpoint for custom images : ANNOTATION
@app.route('/detect/annotation/custom')
def predict_annotation_for_custom_image():
    image_url = request.args.get('url')

    if image_url is None:
        return 'bad request!', 400

    alpha = 0.4

    # Get image
    image = read_image(image_url, isUrl=True)

    # Run prediction
    mask = predict(image, model).astype(np.uint8)
    image = image[0] * 255.0

    # Convert it to grayscale
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    annotation = image.copy()

    # Apply cv2.threshold() to get a binary image
    ret, thresh = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Scale contours
    scaled_contours = []
    for contour in contours:
        scaled_contours.append(scale_contour(contour, 1.075))

    h, w, _ = image.shape

    # Draw contours
    cv2.drawContours(annotation, scaled_contours, -1, (38, 166, 154, 0.1), math.floor(20 / (1225 / 966) * (h / w)), cv2.LINE_AA)

    # Make contours a bit transparent
    annotation = cv2.addWeighted(image, alpha, annotation, 1 - alpha, 0)

    # Send prediction as JPEG
    retval, buffer = cv2.imencode('.jpg', annotation.astype(np.uint8))
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'

    return response


if __name__ == '__main__':
    app.run()
