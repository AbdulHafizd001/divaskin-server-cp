import os

class Config:
    GOOGLE_CLOUD_PROJECT = os.getenv("divaskin-bangkit-capstone")
    GOOGLE_CLOUD_CREDENTIALS = os.getenv("C:\\msib-abdul\\divaskin-server\\credentials.json")
    GCS_BUCKET_NAME = os.getenv("bucket-divaskin")

#"GOOGLE_APPLICATION_CREDENTIALS", 