from services.linkedin_oauth_service import LinkedInOAuthService
from services.logger_service import LoggerService
from services.config import Config


class LinkedInService:
    def validate_authentication(self):
        """
        Validates and refreshes the LinkedIn access token if necessary.
        """
        try:
            access_token = self.oauth_service.get_access_token()
            if not access_token:
                raise Exception("Failed to refresh LinkedIn access token.")
            self.access_token = access_token
        except Exception as e:
            raise Exception(f"Error during LinkedIn authentication: {e}")
    
    def __init__(self):
        self.oauth_service = LinkedInOAuthService()
        self.company_id = Config.LINKEDIN_COMPANY_ID
        self.logger = LoggerService()

    def post_to_linkedin(self, content: str, is_company: bool = True):
        """
        Post content to LinkedIn.
        """
        try:
            # Get a valid access token
            access_token = self.oauth_service.get_access_token()

            headers = {
                "Authorization": f"Bearer {access_token}",
                "X-Restli-Protocol-Version": "2.0.0",
                "Content-Type": "application/json",
            }
            author = f"urn:li:organization:{self.company_id}" if is_company else f"urn:li:person:{Config.LINKEDIN_PROFILE_ID}"
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

            response = requests.post(post_url, headers=headers, json=post_data)
            if response.status_code == 201:
                self.logger.log("Post published successfully!")
            else:
                self.logger.log(f"Publishing error: {response.json()}", "error")
        except Exception as e:
            self.logger.log(f"LinkedIn connection error: {e}", "error")
