# Mobile Price Range Prediction API

## Overview

This API predicts the price range of mobile phones based on their specifications using a machine learning model. It's built with `FastAPI`, a web framework which facilitates the creation of RESTful endpoints, and integrates with `MinIO`, an open-source S3 compatible object storage server.

### Model Training

The machine learning model used by this API is trained on a dataset obtained from [this repository](https://raw.githubusercontent.com/kayfilipp/MobilePriceClassification/main/data/train.csv) or from [kaggle](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification). The training process utilizes `sklearn`, a powerful Python library for building machine learning models. This ensures that the API can reliably predict the price range of mobile phones based on various features such as RAM, battery power, and others as specified in the dataset.

### MinIO Installation and Configuration

To install `MinIO` and set it up for use with this API, please follow the detailed instructions provided in the [official MinIO documentation](https://min.io/docs/minio/container/operations/installation.html).