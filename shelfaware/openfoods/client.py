"""
Client to interact with the Open Food Facts API using a session with optional caching.
"""

import requests
from .food import FoodProduct
from PIL import Image
from io import BytesIO


class OpenFoodClient:
    """
    Client for fetching food product information from the Open Food Facts API.
    
    Uses a requests session to enable caching without globally affecting other requests.
    
    Methods:
        fetch_product: Fetches product details by barcode.
    """
    
    def __init__(self, cache=True, cache_name="openfoods_cache", api_url="https://world.openfoodfacts.org/api/v0/product/"):
        """
        Initializes the OpenFoodClient with an optional cache and custom API URL.
        
        Args:
            cache (bool): Whether to enable caching. Defaults to True.
            cache_name (str): Name of the cache file if caching is enabled. Defaults to "openfoods_cache".
            api_url (str): The base URL for the Open Food Facts API. Defaults to "https://world.openfoodfacts.org/api/v0/product/".
        """
        self.session = requests.Session()

        if cache:
            import requests_cache
            self.session = requests_cache.CachedSession(cache_name)
        
        self.api_url = api_url

    def fetch_product(self, code):
        """
        Fetches product information from Open Food Facts by barcode.
        
        Args:
            code (str): The barcode of the product.
            
        Returns:
            FoodProduct: Instance of FoodProduct with product details, or None if not found.
        """
        response = self.session.get(self.api_url + f"{code}.json")
        food_info = response.json()

        if food_info.get("status") != 1:
            return None

        product = food_info["product"]
        return FoodProduct(
            product_name=product.get("product_name"),
            brands=[tag.replace('en:', '') for tag in product.get('brands_tags', [])],
            categories=[tag.replace('en:', '') for tag in product.get('categories_tags', [])],
            image_url=product.get('image_front_url')
        )

    def fetch_image(self, product):
        """
        Fetches and displays the product image.
        
        Args:
            product (FoodProduct): The product object with an image URL.
        """
        if product.image_url:
            response = self.session.get(product.image_url)
            img = Image.open(BytesIO(response.content))
            img.show()
