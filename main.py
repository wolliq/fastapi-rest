# main.py
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

from typing import List

import torch
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import torch.nn as nn


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


# Define the input data model
class InputData(BaseModel):
    data: List[float]
    # data: List[List[float]]


# Define your PyTorch model and load the weights
class YourModel(torch.nn.Module):
    def __init__(self):
        super(YourModel, self).__init__()
        # Define your model architecture here

    def forward(self, x):
        # Define the forward pass of your model here
        return x


# Define the model
model = nn.Sequential(
    nn.Linear(8, 24),
    nn.ReLU(),
    nn.Linear(24, 12),
    nn.ReLU(),
    nn.Linear(12, 6),
    nn.ReLU(),
    nn.Linear(6, 1)
)
# Later to restore:
filepath = "reg.pt"
model.load_state_dict(torch.load(filepath))
model.eval()

# Create the FastAPI app
app = FastAPI()


# Define the scoring endpoint
@app.post("/score")
async def score(input_data: InputData):
    # Convert the input data to a PyTorch tensor
    input_tensor = torch.tensor(input_data.data)
    logger.info(f"input_tensor: {input_tensor}")

    # Perform the forward pass to get the predictions
    with torch.no_grad():
        output = model(input_tensor)

    # Convert the predictions to a list
    predictions = output.tolist()
    logging.info(f"predictions: {predictions}")

    # Return the predictions as the API response
    return {"predictions": predictions}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
