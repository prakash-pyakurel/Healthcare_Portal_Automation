from database import SessionLocal, Claim
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from selenium_scraper import extract_claims_data
import logging 

# Setup for Logging
logging.basicConfig(filename='./logs/api_access.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Creating FastAPI app
app = FastAPI()

# Security - Simple API Key for Practice/Demo Only 
API_KEY = "secureapikey123"
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key


@app.get("/claims", dependencies=[Depends(verify_api_key)])
def get_claims_data():
    logging.info("Claims data accessed via API.")
    data = extract_claims_data()
    return {"claims": data}


@app.post("/trigger-scrape", dependencies=[Depends(verify_api_key)])
def trigger_scrape():
    logging.info("Triggered manual data scrape and storage.")
    data = extract_claims_data()   # This will runs Selenium to get the latest data from the portal

    db = SessionLocal()            # This opens a connection to your DB (We are using SQLite for Practice/Demo only)
    for claim in data:
        db_claim = Claim(
            patient_id=claim["Patient ID"],
            name=claim["Name"],
            service_date=claim["Service Date"],
            billing_code=claim["Billing Code"]
        )
        db.add(db_claim)
    db.commit()
    db.close()

    return {"message": "Scrape and save completed successfully.", "records_saved": len(data)} 
