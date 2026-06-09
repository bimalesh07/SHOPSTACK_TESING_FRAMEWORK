import os
from dotenv import load_dotenv

# Yeh command root directory se .env file ko load karegi
load_dotenv()

class ReadEnv:
    
    @staticmethod
    def get_api_base_url():
        """Backend API ka main Base URL nikalne ke liye"""
        return os.getenv("API_BASE_URL")

    @staticmethod
    def get_test_user():
        """Test user ka email lane ke liye"""
        return os.getenv("API_TEST_USER")

    @staticmethod
    def get_test_password():
        """Test user ka password lane ke liye"""
        return os.getenv("API_TEST_PASSWORD")