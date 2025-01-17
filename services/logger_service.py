import logging
import os
import json
from datetime import datetime

class LoggerService:
    def __init__(self, name="LinkedInBot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logs = []
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def log(self, message, level="info"):
        if level == "info":
            self.logger.info(message)
            self.logs.append({"level": "INFO", "message": message})
        elif level == "error":
            self.logger.error(message)
            self.logs.append({"level": "ERROR", "message": message})

        self.save_logs_to_file()

    def save_logs_to_file(self):
        log_file = "post_logs.json"
        try:
            if os.path.exists(log_file):
                with open(log_file, "r") as file:
                    logs = json.load(file)
            else:
                logs = []

            logs.append({"timestamp": str(datetime.now()), "logs": self.logs})

            with open(log_file, "w") as file:
                json.dump(logs, file, indent=4)
        except Exception as e:
            print(f"Error saving logs: {e}")
