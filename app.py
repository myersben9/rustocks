import asyncio
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from google.protobuf.message import DecodeError
import PricingData_pb2  # Import your protobuf file here
import yfetch  # Import your yfetch module here
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Write a GET endpoint that retrieves the data for a given ticker with range and interval
# This is correct:
@app.get("/get_data")
def get_data(ticker: str, range: str = "1d", interval: str = "5m"):
    """
    Fetches data for a given ticker using yfetch module.
    """ 
    yf = yfetch.Yfetch([ticker], range=range, interval=interval)
    yf.fetch_data()
    df = yf.df
    # include the index in the dict
    df.reset_index(inplace=True)
    print(df.to_dict(orient='records'))
    return df.to_dict(orient='records')  # Convert DataFrame to dictionary for JSON serialization