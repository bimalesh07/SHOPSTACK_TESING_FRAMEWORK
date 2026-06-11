from selenium.webdriver.common.by import By
from Utilities.customLogger import LogGen
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageObjects.LoginPage import LoginPage
import time

class AddCartPage:
    Add_to_collection = "//span[normalize-space()='Add to Collection']"
    item_increase ="//body/div[@id='root']/div[@class='flex flex-col min-h-screen transition-colors duration-300 bg-white text-slate-900']/main[@class='flex-grow']/div[@class='min-h-screen bg-white dark:bg-slate-950 transition-colors duration-500 overflow-x-hidden']/div[@class='max-w-5xl mx-auto px-4 sm:px-6 pt-4 pb-16 lg:pt-8 lg:pb-24 selection:bg-slate-900 selection:text-white dark:selection:bg-white dark:selection:text-slate-950']/div[@class='lg:grid lg:grid-cols-2 lg:gap-x-16 lg:items-start']/div[@class='mt-12 px-1 sm:px-0 lg:mt-0 space-y-10']/div[2]"
    Toast_message = "//div[@role='status']"


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = LogGen.loggen()

    def add_to_cart(self, quanty):
        self.logger.info("Opening the Product Details page for add to cart")
        plus_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.item_increase)))
        for i in range(quanty):
            plus_btn.click()
            time.sleep(0.5)
            self.logger.info(f"Clicked the Product:{i+1} time(s)")
        self.logger.info(f"Click on 'Add to Collection', button ")

        add_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.Add_to_collection)))
        try:
            add_btn.click()

        except Exception as e:
            self.logger.warn(f"Normal click intercepted due to: {e}. Switching to JavaScript Click Pipeline...")
            self.driver.execute_script("arguments[0].click();", add_btn)

    def got_toast_message_text(self):
        self.logger.info("Here matching with toast Message ")
        try:
            toast = self.wait.until(EC.presence_of_element_located((By.XPATH, self.Toast_message)))
            self.logger.info(f"Toast message find {toast}")
            return toast.text
        except Exception as e:
            self.logger.info("Toast message did not appear")
            return None







        


