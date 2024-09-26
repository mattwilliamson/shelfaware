"""
Food-related classes for interacting with Open Food Facts API.
"""

class FoodProduct:
    """
    Represents a food product fetched from the Open Food Facts API.
    
    Attributes:
        product_name (str): Name of the product.
        brands (list): List of brand tags.
        categories (list): List of category tags.
        image_url (str): URL of the product's image.
    """
    def __init__(self, product_name, brands, categories, image_url):
        self.product_name = product_name
        self.brands = brands
        self.categories = categories
        self.image_url = image_url

    def __repr__(self):
        return f"<FoodProduct(name={self.product_name}, brands={self.brands}, categories={self.categories})>"
