import tensorflow as tf
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# загрузка модели
model = tf.keras.models.load_model('/app/model.h5')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    with open('image.jpg', 'wb') as f:
        f.write(contents)
    preds = process_image('image.jpg')
    return {'predictions': preds.tolist()}

def process_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = x / 255
    x = tf.expand_dims(x, axis=0)
    preds = model.predict(x)
    # здесь можно обработать предсказания нейросети и вернуть результаты
    return preds

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
