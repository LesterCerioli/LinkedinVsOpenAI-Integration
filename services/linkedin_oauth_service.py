import requests
import os
import json
from datetime import datetime, timedelta
from services.config import Config
from services.logger_service import LoggerService

class LinkedInOAuthService:
    def __init__(self):
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        self.redirect_uri = Config.LINKEDIN_REDIRECT_URI
        self.token_file = "linkedin_token.json"
        self.logger = LoggerService()

    def generate_authorization_url(self):
        """
        Generate the LinkedIn OAuth2 authorization URL.
        """
        scopes = "w_member_social r_liteprofile r_emailaddress"
        url = (
            f"https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={scopes}"
        )
        self.logger.log(f"Authorization URL: {url}")
        return url

    def exchange_code_for_access_token(self, authorization_code):
        """
        Exchange the authorization code for an access token.
        """
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            token_data["expires_at"] = (datetime.now() + timedelta(seconds=token_data["expires_in"])).isoformat()
            self.save_token(token_data)
            return token_data["access_token"]
        else:
            self.logger.log(f"Error exchanging code: {response.json()}", "error")
            raise Exception(f"Error exchanging code: {response.json()}")

    def refresh_access_token(self):
        """
        Automatically refresh the access token using client credentials.
        """
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            token_data["expires_at"] = (datetime.now() + timedelta(seconds=token_data["expires_in"])).isoformat()
            self.save_token(token_data)
            self.logger.log("Access token refreshed successfully.")
            return token_data["access_token"]
        else:
            self.logger.log(f"Error refreshing access token: {response.json()}", "error")
            raise Exception(f"Error refreshing access token: {response.json()}")

    def save_token(self, token_data):
        """
        Save token data to a JSON file.
        """
        with open(self.token_file, "w") as file:
            json.dump(token_data, file, indent=4)

    def load_token(self):
        """
        Load token data from a JSON file.
        """
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as file:
                return json.load(file)
        return None

    def is_token_valid(self, token_data):
        """
        Check if the token is still valid based on its expiration time.
        """
        if not token_data:
            return False
        expires_at = datetime.fromisoformat(token_data["expires_at"])
        return datetime.now() < expires_at

    def get_access_token(self):
        """
        Get a valid access token, refreshing if necessary.
        """
        token_data = self.load_token()
        if token_data and self.is_token_valid(token_data):
            return token_data["access_token"]
        else:
            self.logger.log("Access token is expired or missing. Refreshing...")
            return self.refresh_access_token()
