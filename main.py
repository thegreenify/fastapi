import boto3
import os
import logging
from fastapi import FastAPI, HTTPException, Query, Header
from pydantic import BaseModel
from typing import Optional
from mangum import Mangum

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# API key from environment
REQUIRED_API_KEY = os.getenv("API_KEY")

# DynamoDB setup
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("DDB_TABLE"))

app = FastAPI()

class AllotteeResponse(BaseModel):
    aan: str
    allottee_name: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    employer_code_by_employee: Optional[str]
    aadhaar: Optional[str]
    quarter_type: Optional[str]
    address: Optional[str]
    pan: Optional[str]
    date_of_allotment: Optional[str]
    quarter_allotted_to: Optional[str]
    quarter_owned_by: Optional[str]
    custodian: Optional[str]
    current_office: Optional[str]

def verify_api_key(x_api_key: Optional[str]):
    if REQUIRED_API_KEY and x_api_key != REQUIRED_API_KEY:
        logger.warning("Invalid API key provided")
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/api/allottee/{aan}", response_model=AllotteeResponse)
def get_allottee_by_path(aan: str, x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)
    try:
        response = table.get_item(Key={"aan": aan})
        if "Item" in response:
            logger.info(f"AAN {aan} fetched successfully")
            return response["Item"]
        logger.info(f"AAN {aan} not found in table")
        raise HTTPException(status_code=404, detail="Allottee not found")
    except Exception as e:
        logger.error(f"Error fetching AAN {aan}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/allottee/search", response_model=AllotteeResponse)
def search_allottee(aan: Optional[str] = Query(None), x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)
    if not aan:
        raise HTTPException(status_code=400, detail="AAN is required")
    return get_allottee_by_path(aan, x_api_key)

handler = Mangum(app)
