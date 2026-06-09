import os
import pytest
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="class")
def setup(request):
    print("Opening Chrome Broswer")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    # get a acess Baseclass
    if request.cls is not None:
        request.cls.driver = driver
    
    yield driver

    print("Broswers window  close after class completed")


# need Fresh url so here remove cokies

@pytest.fixture(scope="function", autouse=True)
def fresh_url(request):
    if hasattr(request.cls, 'driver'):
        base_url = os.getenv("SHOPSTACK_BASE_URL", "https://shopstack-ecommerce.vercel.app")
        print("Fresh url cleaing seeion cookies and hitting Fresh Url")
        request.cls.driver.delete_all_cookies()
        request.cls.driver.get(base_url)





