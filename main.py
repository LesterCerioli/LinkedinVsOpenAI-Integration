import uvicorn
from services.chatgpt_service import ChatGPTService
from services.linkedin_service import LinkedInService
from services.logger_service import LoggerService

logger = LoggerService()

def run_worker():
    chatgpt = ChatGPTService()
    linkedin = LinkedInService()

    prompt = "Crie uma postagem promovendo um software médico inovador que melhora a eficiência dos hospitais."
    post_content = chatgpt.generate_post(prompt)

    if post_content:
        logger.log("Starting posting on personal profile...")
        linkedin.post_to_linkedin(post_content, is_company=False)

        logger.log("Starting posting on company page...")
        linkedin.post_to_linkedin(post_content, is_company=True)

if __name__ == "__main__":
    logger.log("Starting LinkedIn worker...")
    run_worker()

    logger.log("Starting FastAPI server to show logs...")
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000)

