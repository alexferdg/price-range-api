# Data science pipeline: Fetch, preprocess, train, and upload a model to Minio
import os
from dotenv import dotenv_values
from minio import Minio
from minio.error import S3Error
import io
import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pickle
import json


# Environment variables for Minio connection
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
env_file_path = os.path.join(parent_dir, ".env")
config = dotenv_values(env_file_path)

# Initialize Minio client
minio_client = Minio(
        config["MINIO_ENDPOINT"],
        access_key=config["MINIO_ACCESS_KEY"],
        secret_key=config["MINIO_SECRET_KEY"],
        secure=False
)

# Reproducibility
SEED = 7

# Function to fetch and merge data chunks, excluding specified dates
def fetch_and_merge_chunks(exclude_dates=[]):
    chunks = []
    try:
        objects = minio_client.list_objects(bucket_name="rawdata", recursive=True) 
        for obj in objects:
            obj_name = obj.object_name
            date_ = obj_name.split("/")[1] # rawdata/2023-02-04/train_chunk_2.csv
            if date_ in exclude_dates:
                continue 
            minio_data = minio_client.get_object("rawdata", obj_name)
            chunk = minio_data.data
            chunk_df = pd.read_csv(io.StringIO(chunk.decode("utf-8"))) 
            chunks.append(chunk_df)
    except S3Error as err:
        print(err)
    final_df = pd.concat(chunks, ignore_index=True)
    return final_df

# Fetch and preprocess data
df = fetch_and_merge_chunks(exclude_dates=["2023-09-14"]) 
df.fillna(df.mean(), inplace=True) 

# Data visualization
df.hist(figsize=(15, 13)) 
plt.show()

# Normalize the data
scaler = StandardScaler()
x = scaler.fit_transform(df.drop(columns=["price_range"])) 
y = df["price_range"].values

# Split data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=SEED)

# Generate a unique model_id using a timestamp
model_id = datetime.now().strftime("%Y%m%d%H%M%S") 

# Train a RandomForestClassifier
model = RandomForestClassifier(random_state=SEED)
model.fit(x_train, y_train)

# Predict and calculate accuracy
y_pred = model.predict(x_test)
rf_acc = accuracy_score(y_test, y_pred)
print(f"Random Forest Accuracy: {rf_acc}")

# Serialize and upload the trained model to Minio
model_filename = f"mpc_model_{model_id}.pkl"
mpc_models_path = os.path.join(parent_dir, "mpc_models")
model_filename_path = os.path.join(mpc_models_path, model_filename)

with open(model_filename_path, "wb") as file:
    pickle.dump(model, file) 

bucket_name = "models"
if not minio_client.bucket_exists(bucket_name=bucket_name):
    minio_client.make_bucket(bucket_name=bucket_name)

try:
    minio_client.fput_object(bucket_name, model_filename, model_filename_path)
except S3Error as err:
    print(err)

# Model metrics as JSON to Minio using model_id in the filename
metrics = {"accuracy": rf_acc}
metrics_json = json.dumps(metrics).encode('utf-8')
metrics_filename = f"metrics_{model_id}.json"
metrics_bucket = "model-metrics"

try:
    if not minio_client.bucket_exists(bucket_name=metrics_bucket):
        minio_client.make_bucket(bucket_name=metrics_bucket)
        print(f"Bucket '{metrics_bucket}' created successfully.")

    minio_client.put_object(
        bucket_name=metrics_bucket,
        object_name=metrics_filename,
        data=io.BytesIO(metrics_json),
        length=len(metrics_json),
        content_type='application/json'
    )
except S3Error as err:
    print(f"Error creating bucket '{metrics_bucket}': {err}")