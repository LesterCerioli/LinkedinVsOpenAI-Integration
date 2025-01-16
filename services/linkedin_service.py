import requests
from services.config import Config
from services.logger_service import LoggerService

class LinkedInService:
    def __init__(self):
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN
        self.profile_id = Config.LINKEDIN_PROFILE_ID
        self.company_id = Config.LINKEDIN_COMPANY_ID
        self.logger = LoggerService()

    def post_to_linkedin(self, content: str, is_company: bool = False):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        author = f"urn:li:organization:{self.company_id}" if is_company else f"urn:li:person:{self.profile_id}"
        post_url = "https://api.linkedin.com/v2/ugcPosts"

        post_data = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        try:
            response = requests.post(post_url, headers=headers, json=post_data)
            if response.status_code == 201:
                self.logger.log("Post published successfully!")
            else:
                self.logger.log(f"Publishing error: {response.json()}", "error")
        except Exception as e:
            self.logger.log(f"LinkedIn connection error: {e}", "error")
