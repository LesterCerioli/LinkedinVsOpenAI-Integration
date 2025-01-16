import logging

class LoggerService:
    def __init__(self, name="LinkedInBot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        self.logs = []
        
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        handler.setLevel(logging.INFO)
        
        self.logger.addHandler(handler)

    def log(self, message, level="info"):
        if level == "info":
            self.logger.info(message)
            self.logs.append({"level": "INFO", "message": message})
        elif level == "error":
            self.logger.error(message)
            self.logs.append({"level": "ERROR", "message": message})
        elif level == "warning":
            self.logger.warning(message)
            self.logs.append({"level": "WARNING", "message": message})

    def get_logs(self):
        return self.logs
