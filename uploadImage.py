from google.cloud import storage
import wget
import io
import os

project_id = "ru-hack-2020"
bucket_name = "ruhack2020"
destination_name = "ingredients"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'KEY.json'
storage_client = storage.Client()

source_file = "https://cdn.shopify.com/s/files/1/0050/0036/4150/articles/healthy_fats_horizontal_1024x1024.jpg"


def upload(bucket_name, source_file, destination_name):
    filename = wget.download(source_file)

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(filename, content_type="image/jpg")
    os.remove(filename)


upload(bucket_name, source_file, destination_name)