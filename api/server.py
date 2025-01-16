from fastapi import FastAPI
from services.logger_service import LoggerService

app = FastAPI()
logger = LoggerService()

@app.get("/")
def health_check():
    return {"status": "ok", "message": "FastAPI server is running"}

@app.get("/logs")
def get_logs():
    return {"logs": logger.get_logs()}
