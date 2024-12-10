from google.cloud import storage
import requests
from io import BytesIO
import urllib.parse

# Google Cloud Storage configurations
BUCKET_NAME = "bucket-divaskin"

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

    # Decode the URL to get the original file name
    blob_name = urllib.parse.unquote(file_url.split('/')[-1])
    print(f"Attempting to delete: {blob_name}")
    
    blob = bucket.blob(blob_name)
    blob.delete()

def fetch_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    return BytesIO(response.content)
