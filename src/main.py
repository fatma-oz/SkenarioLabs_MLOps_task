import logging.config
import pickle
import os

import pandas as pd
import numpy as np
from fastapi import FastAPI

from request_item import RequestItem

import monitoring_testing

logger = logging.getLogger(__name__)
app = FastAPI()

logging.error(os.getcwd())

with open(f'{os.getcwd()}/model/model.pickle', 'rb') as handle:
    model = pickle.load(handle)

    
#@app.post    
    
@app.get('/')     #predict
async def valuate(request: RequestItem):
    df = pd.DataFrame([request.__dict__])
    y = model.predict(df.values.tolist())
    
    results = checking.monitoring_testing([request.__dict__])
    return {'prediction': round(np.exp(y[0]), -2)  , "results": results }
