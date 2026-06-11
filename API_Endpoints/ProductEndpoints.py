import requests

class ProductEndpoints:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_all_products(self, params= None):
        """Public fetch list of all products(no Login Required)"""

        url= f"{self.base_url}/products/"
        response = requests.get(url, params=params)
        return response
    
    def get_product_by_id(self, product_id):
        """Public Fetch detilas of single product using(No Login Required)"""
        url = f"{self.base_url}/products/{product_id}"
        response = requests.get(url)
        return response
    
    def get_all_categrories(self):
        """Public Fecth list of all proucts categeory (No Login Required)"""
        url = f"{self.base_url}/products/categories"
        response = requests.get(url)
        return response
        