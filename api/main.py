from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI(title="Sales-Fusion API", version="1.0.0")

# 8.5 Security/Authentication Stub
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    if token != "super_secret_dev_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

# 8.4 API Layer Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Sales-Fusion Agentic API"}

@app.post("/token")
def login(form_data: dict):
    # Stub for JWT logic
    return {"access_token": "super_secret_dev_token", "token_type": "bearer"}

@app.get("/forecast/revenue", dependencies=[Depends(verify_token)])
def get_revenue_forecast():
    """Retrieve the latest Prophet revenue forecast."""
    file_path = "reports/forecasts/revenue_forecast.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return {"forecast": df.tail(10).to_dict(orient="records")}
    raise HTTPException(status_code=404, detail="Forecast not found")

@app.get("/insights/anomalies", dependencies=[Depends(verify_token)])
def get_regional_anomalies():
    """Retrieve detected regional anomalies."""
    file_path = "reports/insights/regional_anomalies.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return {"anomalies": df.to_dict(orient="records")}
    raise HTTPException(status_code=404, detail="Anomalies not found")
