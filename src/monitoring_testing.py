import pandas as pd
import numpy as np
import requests

# Define the endpoint for making predictions
PREDICTION_ENDPOINT = "http://localhost:8080/predict"

# Define the parameters for monitoring
INPUT_COLUMNS = ['bed', 'bath', 'acre_lot', 'zip_code', 'house_size']
MISSING_THRESHOLD = 0.1 # 10% missing data is the threshold for flagging
PREDICTION_DISTRIBUTION_THRESHOLD = 0.1 # 10% difference in distribution is the threshold for flagging


# Define a function to make a prediction
def make_prediction(data):
    data = data.to_json()
    response = requests.post(PREDICTION_ENDPOINT, json=data)
    return response.json()

# Define a function to check the missing input parameter rate
def check_missing_rate(data):
    num_missing = data.isnull().sum().sum()
    num_total = data.size
    missing_rate = num_missing / num_total
    if missing_rate > MISSING_THRESHOLD:
        print(f"Warning: Missing input parameter rate is {missing_rate:.2f}, which exceeds the  threshold of {MISSING_THRESHOLD:.2f}")

# Define a function to check the prediction distribution
def check_prediction_distribution(data):
    preds = make_prediction(data)
    distribution = pd.Series(preds).value_counts(normalize=True)
    reference_distribution = pd.Series(np.ones(len(distribution))/len(distribution), index=distribution.index)
    kl_divergence = (distribution * np.log(distribution / reference_distribution)).sum()
    if kl_divergence > PREDICTION_DISTRIBUTION_THRESHOLD:
        print(f"Warning: Prediction distribution is significantly different from the reference distribution, with KL-divergence of {kl_divergence:.2f}")

# Define a function to load the data
def load_data():
    data =pd.DataFrame([request.__dict__])                 
    return data[INPUT_COLUMNS]

# Define the checking function
def checking():
    data = load_data()
    check_missing_rate(data)
    check_prediction_distribution(data)
    return data, check_missing_rate, check_prediction_distribution

    

    