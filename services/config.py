import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

class Config:
    # Variáveis do LinkedIn
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
    LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
    LINKEDIN_COMPANY_ID = os.getenv("LINKEDIN_COMPANY_ID")

    # Variáveis do OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Testar se as variáveis foram carregadas (fora da classe)
if __name__ == "__main__":
    print("LINKEDIN_CLIENT_ID:", Config.LINKEDIN_CLIENT_ID)
    print("LINKEDIN_CLIENT_SECRET:", Config.LINKEDIN_CLIENT_SECRET)
    print("LINKEDIN_REDIRECT_URI:", Config.LINKEDIN_REDIRECT_URI)
    print("LINKEDIN_COMPANY_ID:", Config.LINKEDIN_COMPANY_ID)
    print("OPENAI_API_KEY:", Config.OPENAI_API_KEY)
