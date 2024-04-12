# Download a dataset from the internet and upload it to Minio
from datetime import datetime, timedelta
import random
import pandas as pd
from minio import Minio
from minio.error import S3Error
import subprocess
import os
from dotenv import dotenv_values
import io


# Environment variables for Minio connection
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
env_file_path = os.path.join(parent_dir, ".env")
config = dotenv_values(env_file_path)

def generate_random_date():
    # Generate a random date between two dates
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    random_date = start_date + timedelta(days=random_days)

    return random_date

# Initialize Minio client
minio_client = Minio(
        config["MINIO_ENDPOINT"],
        access_key=config["MINIO_ACCESS_KEY"],
        secret_key=config["MINIO_SECRET_KEY"],
        secure=False
)

bucket_name = "rawdata"

if not minio_client.bucket_exists(bucket_name=bucket_name):
    minio_client.make_bucket(bucket_name=bucket_name)

url = 'https://raw.githubusercontent.com/kayfilipp/MobilePriceClassification/main/data/train.csv' # or the kaggle link: https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification
file_path = '/Users/alex/data/minio-data/rawdata/mobile_train.csv'
os.makedirs(os.path.dirname(file_path), exist_ok=True)
result = subprocess.run(['curl', '-o', file_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if result.returncode == 0:
    print(f"Successfully downloaded the file to {file_path}")
else:
    print(f"Failed to download the file: {result.stderr.decode('utf-8')}")

df = pd.read_csv(file_path)

print(f"Total records downloaded: {len(df)}")

chunk_size = 100

chunks = [
    df[i:i+chunk_size] for i in range(0, len(df), chunk_size)
]

for i, chunk in enumerate(chunks):
    # <bucket>/<object_name>
    # rawdata/<date>/train_chunk_<i>.csv
    random_date = generate_random_date().strftime("%Y-%m-%d")
    object_name = f"{random_date}/train_chunk_{i}.csv"

    try:
        csv_date = chunk.to_csv(index=False).encode("utf-8")
        csv_stream = io.BytesIO(csv_date)

        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=csv_stream,
            length=len(csv_date),
            content_type="text/csv"
        )
        print(f"Chunk {i} stored as {object_name}")
    except S3Error as err:
        print(err)