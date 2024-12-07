from google.cloud import storage
import tensorflow as tf
import numpy as np
from PIL import Image
import requests

# Load model globally to avoid reloading
model = tf.keras.models.load_model("model/model.h5")

# Google Cloud Storage configurations
BUCKET_NAME = "your-bucket-name"

def upload_to_gcs(file):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url

def delete_from_gcs(file_url):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob_name = file_url.split('/')[-1]
    blob = bucket.blob(blob_name)
    blob.delete()

def classify_skin_type(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    classes = ["Oily", "Dry", "Normal"]
    return classes[np.argmax(prediction)]
