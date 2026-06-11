import time
from Test_Case.basetest import BaseTest
from PageObjects.AddCartPage import AddCartPage
from PageObjects.LoginPage import LoginPage
from PageObjects.ProductCartPage import ProductCartPage 
from Utilities.customLogger import LogGen
import os

class Test_Add_To_Cart(BaseTest):
    user_email = os.getenv("LOGIN_USERNAME") if os.getenv("LOGIN_USERNAME") else "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") if os.getenv("LOGIN_PASSWORD") else "Password@123"
    logger = LogGen.loggen()

    # 🟢 FIX 1: ', driver' hata diya hai yahan se
    def test_login_and_add_to_cart_limit(self):
        self.logger.info("********** Starting Add to cart Test ******************")

        """Login Process"""
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, self.user_password)
        
        # OTP dalne ke liye sleep pehle lagayein taaki validation baad me ho
        self.logger.info("⏳ OTP WAITING BUFFER: Enter OTP manually right now...")
        time.sleep(15)
        
        assert lp.is_logout_button_visible() == True, "ERROR: LOGIN Are Not Working"
        self.logger.info("Login is successfully")

        """Navigate the Shop the page Prerequested """
        pc = ProductCartPage(self.driver)
        pc.navigate_to_shop_page()
        
        # 🟢 FIX 2: () Brackets lagaye hain function call ke liye
        pc.click_product_to_open_details()

        """Confirm its work or not """
        assert pc.is_details_page_opened_successfully() == True, "Step Error: Target details view did not open"
        self.logger.info("Loading confirmed, handing over control to AddCartPage")

        """Addtocart Page cart functional testing """
        ap = AddCartPage(self.driver)
        self.logger.info("Test Step A: Selecting 5 units and clicking add to collection")
        ap.add_to_cart(4)

        """Verify the Toast"""
        # 🟢 FIX 3: 'got' ko badal kar 'get' kiya hai
        toast_success = ap.get_toast_message_text()

        assert toast_success is not None, "Test Failed: Success toast notification did not show"
        
        # 🟢 FIX 4: Assertion condition ko clean kiya hai
        toast_lower = toast_success.lower()
        assert "added" in toast_lower or "success" in toast_lower or "cart" in toast_lower, \
                f"Test Failed: Unexpected toast String capture : {toast_success}"
        
        self.logger.info(f"🟢 STEP A PASSED: Toast notification verified -> {toast_success}")

        """Page Refresh"""
        self.logger.info("Refreshing browser to sync backend cart state")
        self.driver.refresh()
        time.sleep(3)

        """If the product is available like 10 then the same user added 7 item in cart
           then if the add to cart like 8 then the message is product is not available"""
        
        self.logger.info("Test Step B: Attempting to select 8 more units to break the unit inventory")
        ap.add_to_cart(7)

        """Verify the out Of Stock """
        # 🟢 FIX 3: 'got' ko badal kar 'get' kiya hai
        toast_error = ap.get_toast_message_text()
        assert toast_error is not None, "Test Failed: Error toast notification did not show for stock overflow"

        """Assertion to ensure websites throws the right error message"""
        assert "not stock" in toast_error.lower() or "out of stock" in toast_error.lower() or "available" in toast_error.lower(), \
                f"❌ Test Failed: System allowed extra items or gave wrong message: '{toast_error}'"
                
        self.logger.info(f"🟢 STEP B PASSED: Stock boundary limit successfully enforced by system -> {toast_error}")
        self.logger.info("*********** END SUITE: ADDCARTPAGE STACK EVALUATED WITH 100% SUCCESS ***********")