# 👉 File: Utilities/customLogger.py
import logging
import os

class LogGen:
    """This is for Ui"""
    @staticmethod
    def loggen():
        if not os.path.exists(".\\Logs"):
            os.makedirs(".\\Logs")
        logger = logging.getLogger("ShopStackAutomation")
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.setLevel(logging.INFO)
        
        # 🔥 FIX: Added encoding='utf-8' here
        file_handler = logging.FileHandler(".\\Logs\\automation.log", mode='a', encoding='utf-8')
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
    
    #This is For API
    @staticmethod
    def apiloggen():
        if not os.path.exists(".\\Logs"):
            os.makedirs(".\\Logs")
            
        # Naya unique naam diya taaki UI ke sath mix na ho
        api_logger = logging.getLogger("ShopStackAPI") 
        
        if api_logger.hasHandlers():
            api_logger.handlers.clear()
            
        api_logger.setLevel(logging.INFO)
        
        # automation api .log
        api_file_handler = logging.FileHandler(".\\Logs\\automation_api.log", mode='a', encoding='utf-8')
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        api_file_handler.setFormatter(formatter)
        api_logger.addHandler(api_file_handler)
        
        return api_logger