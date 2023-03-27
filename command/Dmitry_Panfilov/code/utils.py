# Under Reconstruction!!

import os
import json
import requests
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
#from tensorflow.keras.metrics import dice_coef
from tensorflow.keras.optimizers import Adam
from fastapi import FastAPI, File, UploadFile, Form, Depends



#model = load_model('model.h5')


def process_image(image_path):
    """Нужно возвращать переменную results в виде BytesIO или base64 строки"""
    try:
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = x / 255
        x = tf.expand_dims(x, axis=0)
        results = model.predict(x)
        return results.tolist()
    except Exception as e:
        return {"error": str(e)}

def imager(img_url: str) -> dict:
    image_response = requests.get(img_url)
    if image_response.status_code == 200:
        with open("image.jpg", "wb") as f:
            f.write(image_response.content)
        results = process_image("image.jpg")
        # if "error" in results:
        #     return {"code": 400, "message": results["error"]}
    else:
        return {"code": 400, "message": 'Не удалось загрузить изображение!'}

    try:
        return {"code": 200, "message": "OK", "image": results}
    except Exception as e:
        return {"code": 400, "message": str(e)}
