import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.customLogger import LogGen

class CheckoutPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = LogGen.loggen()
    
    # --- Locators Grid (Saare standard Tuples mein convert kar diye hain) ---
    cart_nav_path = (By.XPATH, "//*[name()='path' and contains(@d,'M2.05 2.05')]")
    btn_checkout_securely = (By.XPATH, "//span[normalize-space()='Checkout Securely']")
    lbl_preparing_checkout = (By.XPATH, "//p[@class='text-slate-600 font-medium']")
    btn_add_new_address = (By.XPATH, "//button[normalize-space()='+ Add New']")
    
    # Address Form fields
    txt_full_name = (By.XPATH, "//input[@placeholder='John Doe']")
    txt_phone = (By.XPATH, "//input[@placeholder='+91 00000 00000']")
    txt_street = (By.XPATH, "//input[@placeholder='+91 00000 00000']")  # 💡 UI placeholder text check kar lena ek baar
    txt_city = (By.XPATH, "//input[@placeholder='City']")
    txt_state = (By.XPATH, "//input[@placeholder='State']")
    txt_pincode = (By.XPATH, "//input[@placeholder='Pincode']")
    btn_save_address = (By.XPATH, "//button[normalize-space()='Save Address']")
    
    #Existing Saved Address Card
    saved_address_card = (By.XPATH, "//div[contains(@class, 'border-slate-900') or contains(@class, 'shadow-sm')]")
    
    # Payment Options
    opt_cash_on_delivery = (By.XPATH, "//p[normalize-space()='Cash on Delivery']")
    opt_online_payment = (By.XPATH, "//p[normalize-space()='Online Payment']")
    btn_complete_order = (By.XPATH, "//span[normalize-space()='Complete Order']")
    
    # Order Confirmation Header
    lbl_order_placed = (By.XPATH, "//h1[normalize-space()='Order Placed']")

    #Actions / Methods ---

    def click_cart_nav_path(self):
        # *self use karne se tuple open ho jata hai (By.XPATH, "path") ki tarah
        nav_cart = self.wait.until(EC.element_to_be_clickable(self.cart_nav_path))
        self.driver.execute_script("arguments[0].click();", nav_cart)
        self.logger.info("************ Cart Navbar Icon Clicked Successfully ************")

    def click_checkout_securely(self):
        btn_cart = self.wait.until(EC.element_to_be_clickable(self.btn_checkout_securely))
        self.driver.execute_script("arguments[0].click();", btn_cart)
        time.sleep(2)
        self.logger.info("************ Checkout Securely Btn CLICKING Successfully... ************")
    
    def wait_for_check_out_laoder_disapaer(self):
        self.logger.info("******** Checking until Preparing checkout is invisible **********************")
        try:
            #Bug Fixed: invisibility_of_element_located use hota hai tuple ke liye
            self.wait.until(EC.invisibility_of_element_located(self.lbl_preparing_checkout))
        except Exception as e:
            self.logger.error(f"Something went wrong with loader wait: {e}")
        time.sleep(2)

    def handle_shipping_address(self, input_name, input_phone, input_street, input_city, input_state, input_pin):
        """Address check: If present then auto-select/skip, else add fresh address"""  
        try:
            self.wait.until(EC.visibility_of_element_located(self.saved_address_card))
            self.logger.info("Saved Address card present inside DOM, auto skipping form filling!")
            
        except:
            self.logger.info("Shipping Grid is empty! FILLING The address block...")
            
            #Form display karne ke liye + Add New par click kiya
            add_new_btn = self.wait.until(EC.element_to_be_clickable(self.btn_add_new_address))
            self.driver.execute_script("arguments[0].click();", add_new_btn)
            time.sleep(1)

            #Form Data Injection Loop (Bugs Fixed: Variables are not overwritten anymore) ---
            name_field = self.wait.until(EC.visibility_of_element_located(self.txt_full_name))
            name_field.clear()
            name_field.send_keys(input_name)

            phone_field = self.wait.until(EC.visibility_of_element_located(self.txt_phone))
            phone_field.clear()
            phone_field.send_keys(input_phone)
            
            street_field = self.wait.until(EC.visibility_of_element_located(self.txt_street))
            street_field.clear()
            street_field.send_keys(input_street)

            city_field = self.wait.until(EC.visibility_of_element_located(self.txt_city))
            city_field.clear()
            city_field.send_keys(input_city)
            
            state_field = self.wait.until(EC.visibility_of_element_located(self.txt_state))
            state_field.clear()
            state_field.send_keys(input_state)
            
            #Bug Fixed: Yahan full_name ka locator laga tha pehle, ab sahi txt_pincode chalega
            pin_field = self.wait.until(EC.visibility_of_element_located(self.txt_pincode))
            pin_field.clear()
            pin_field.send_keys(input_pin)

            #Save address Form Trigger
            save_btn = self.wait.until(EC.element_to_be_clickable(self.btn_save_address))
            self.driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(3)

    def selected_payment_and_place_order(self, method="COD"):
        #1. PAYMENT METHOD SELECT KARNA ---
        if method.upper() == "COD":
            self.logger.info("************ Selecting Cash on Delivery *****************")
            mode_btn = self.wait.until(EC.element_to_be_clickable(self.opt_cash_on_delivery))
            self.driver.execute_script("arguments[0].click();", mode_btn)
            time.sleep(2)
        
        elif method.upper() == "ONLINE":
            self.logger.info("************ Selecting Online Payment *****************")
            mode_btn = self.wait.until(EC.element_to_be_clickable(self.opt_online_payment))
            self.driver.execute_script("arguments[0].click();", mode_btn)
            time.sleep(2)
            
            #ONLINE ME PEHLE BUTTON CLICK HOGA TAAKI RAZORPAY POPUP KHULE!
            order_btn = self.wait.until(EC.element_to_be_clickable(self.btn_complete_order))
            self.driver.execute_script("arguments[0].click();", order_btn)
            
            # Popup khulne ke baad ab 1 minute rukenge manual payment ke liye
            self.logger.info("***** Wait for Razorpay manual payment (1 Min) **************")
            time.sleep(60)
            self.logger.info("COMPLETED THE PAYMENT BUFFER CYCLE")
            return # Online ka execution yahin se block return ho jayega

        # --- 2. COD KE LIYE FINAL BUTTON CLICK (ROUTING OUTSIDE BLOCK) ---
        order_btn = self.wait.until(EC.element_to_be_clickable(self.btn_complete_order))
        self.driver.execute_script("arguments[0].click();", order_btn)
        time.sleep(3)
        self.logger.info("************ Order Placed via COD Successfully *****************")

    def get_order_status_text(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.lbl_order_placed)).text
        except:
            return None
        