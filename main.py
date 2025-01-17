import schedule
import time
from datetime import datetime
from services.chatgpt_service import ChatGPTService
from services.linkedin_service import LinkedInService
from services.logger_service import LoggerService

logger = LoggerService()

def run_worker():
    """
    Generates a post using ChatGPT and publishes it on LinkedIn.
    """
    try:
        logger.log("Initializing worker...")
        chatgpt = ChatGPTService()
        linkedin = LinkedInService()

        prompt = "Create a post promoting an innovative medical software that improves hospital efficiency."

        # Generate post content
        post_content = chatgpt.generate_post(prompt)

        if post_content:
            logger.log(f"Post content generated: {post_content[:50]}...")  # Log the first 50 characters
            logger.log("Starting LinkedIn post...")
            linkedin.post_to_linkedin(post_content, is_company=True)
            logger.log("Post published successfully!")
        else:
            logger.log("Failed to generate post content. Post content is empty.", "error")
    except Exception as e:
        logger.log(f"Error in worker execution: {e}", "error")

def schedule_posts():
    """
    Schedules posts every hour starting from 16/01/2025 at 20:30.
    """
    try:
        # Validate LinkedIn Authentication
        linkedin = LinkedInService()
        linkedin.validate_authentication()  # Add this to check or refresh the token
        logger.log("LinkedIn authentication validated successfully.")

        # Define the start date and time
        start_date = "2025-01-16"
        start_time = "20:30"
        current_datetime = datetime.now()
        target_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")

        if current_datetime < target_datetime:
            # Wait until the target time
            logger.log(f"Waiting until {target_datetime} to start posting...")
            while datetime.now() < target_datetime:
                time.sleep(10)  # Check every 10 seconds
            logger.log("Starting scheduled posts...")

        # Schedule posts to run every hour
        schedule.every(1).hours.do(run_worker)

        # Infinite loop to keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logger.log(f"Error in scheduler setup: {e}", "error")

if __name__ == "__main__":
    try:
        logger.log("Starting the LinkedIn posting scheduler...")
        schedule_posts()
    except KeyboardInterrupt:
        logger.log("Scheduler stopped manually.", "warning")
    except Exception as e:
        logger.log(f"Unexpected error occurred: {e}", "error")
