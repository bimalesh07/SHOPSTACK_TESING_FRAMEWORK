import time
from Test_Case.basetest import BaseTest
from PageObjects.ProductPage import ProductPage
from Utilities.customLogger import LogGen

class Test_003_Guest_Smoke_Flows(BaseTest):
    logger = LogGen.loggen()

    def test_guest_complete_smoke_journey(self):
        self.logger.info("🧪 ===================================================")
        self.logger.info("🧪 STARTING FINAL STABLE GUEST SMOKE JOURNEY")
        self.logger.info("🧪 ===================================================")
        
        prod = ProductPage(self.driver)

        # 🌓 1. Theme transitions
        prod.click_dark_mode()
        time.sleep(3)
        prod.click_light_mode()
        time.sleep(3)
        
        # 🗺️ 2. Jump directly to Electronics Collection view context
        prod.open_collections_dropdown()
        time.sleep(3)
        
        # 🛍️ 3. Reset display catalog state
        prod.click_shop_navigation()
        time.sleep(2)
        
        # 🔍 4. Search interface lookups
        prod.serach_product("Laptop")
        time.sleep(3)
        
        # ❤️ 5. Guest Auth block validation for Wishlist
        prod.click_heart_icon()
        time.sleep(2)
        assert prod.is_login_page_enforced() == True, "❌ BUG: Welcome back screen failed to initialize!"
        self.logger.info("🎉 SUCCESS: Verified Guest access locked out of Wishlist interaction.")

        # Re-syncing browser state
        self.driver.get("https://shopstack-ecommerce.vercel.app/products")
        time.sleep(2)

        # 👉 6. Details template lookup validation
        prod.click_first_listed_product()
        time.sleep(3)
        assert self.driver.find_element("xpath", prod.text_product_title_xpath).is_displayed() == True, \
            "❌ BUG: Laptop description landing lookups broken!"
        self.logger.info("🎉 SUCCESS: Target metadata loaded smoothly without sessions.")
        
        # 🔒 7. Checkout Guard check
        prod.click_secure_checkout()
        time.sleep(3)
        assert prod.is_login_page_enforced() == True, "❌ BUG: Checkout action leaked bypass access constraints!"
        self.logger.info("🎉 SUCCESS: Guest smoke suite validation execution completed.")
        self.logger.info("🧪 ===================================================")