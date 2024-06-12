from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Message(BaseModel):
    message: str

rules = [
    {"id": "R1", "description": "Monthly pension payments (except member 2752 - annually)", "price": 50},
    {"id": "R2", "description": "Payments in arrears for new retirees and dependants", "price": 30},
    {"id": "R3", "description": "Payment adjustments for holidays", "price": 10},
    {"id": "R4", "description": "Final payment adjustments on death", "price": 100},
    {"id": "R5", "description": "Calculation fee for Normal Retirement Date (NRD)", "price": 200},
    {"id": "R6", "description": "Processing fee for early retirement", "price": 150},
    {"id": "R7", "description": "Fixed 7.5% increase (pre 6/4/1988 GMP)", "price": 25},
    {"id": "R8", "description": "RPI adjustment for post 30/4/1999 benefits", "price": 50},
    {"id": "R9", "description": "Widow/widower pension setup", "price": 100},
]

@app.post("/extract_rules")
async def extract_rules(msg: Message):
    # Simulate rule extraction logic
    extracted_rules = rules  # In a real implementation, this would parse and extract rules
    return {"rules": extracted_rules}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
