import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    LINKEDIN_PROFILE_ID = os.getenv("LINKEDIN_PROFILE_ID")
    LINKEDIN_COMPANY_ID = os.getenv("LINKEDIN_COMPANY_ID")
