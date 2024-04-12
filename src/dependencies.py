# Dependencies for FastAPI application
from fastapi import Depends, HTTPException
import pickle
from minio import Minio
import os
from dotenv import dotenv_values


# Environment variables for Minio connection
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
env_file_path = os.path.join(parent_dir, ".env")
config = dotenv_values(env_file_path)

# Dependency for Minio client
def get_minio_client():
    return Minio(
        config["MINIO_ENDPOINT"],
        access_key=config["MINIO_ACCESS_KEY"],
        secret_key=config["MINIO_SECRET_KEY"],
        secure=False
    )

# Dependency for model loading
def load_model(model_id: str, minio_client: Minio = Depends(get_minio_client)):
    try:
        model_data = minio_client.get_object("models", f"{model_id}").data
        model = pickle.loads(model_data)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))