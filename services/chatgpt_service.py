import openai
from services.config import Config
from services.logger_service import LoggerService

class ChatGPTService:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.logger = LoggerService()

    def generate_post(self, prompt: str) -> str:
        openai.api_key = self.api_key
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            post_content = response["choices"][0]["message"]["content"]
            self.logger.log("Generated post content successfully.")
            return post_content
        except Exception as e:
            self.logger.log(f"Error generating post content: {e}", "error")
            return None
