import unittest
from unittest.mock import patch, Mock
from shelfaware.openfoods.client import OpenFoodClient
from shelfaware.openfoods.food import FoodProduct

# Mock response based on your provided JSON
MOCK_PRODUCT_RESPONSE = {
    "code": "4099100207149",
    "product": {
        "product_name": "Rolled Oats",
        "brands_tags": ["millville", "aldi"],
        "categories_tags": [
            "en:plant-based-foods-and-beverages",
            "en:plant-based-foods",
            "en:breakfasts",
            "en:cereals-and-potatoes",
            "en:cereals-and-their-products",
            "en:breakfast-cereals",
            "en:flakes",
            "en:cereal-flakes",
            "en:rolled-flakes",
            "en:rolled-oats"
        ],
        "image_front_url": "https://images.openfoodfacts.org/images/products/409/910/020/7149/front_en.3.400.jpg"
    },
    "status": 1
}

class TestOpenFoodClient(unittest.TestCase):
    
    @patch('requests.get')
    def test_fetch_product_success(self, mock_get):
        # Mock the response with your mock data
        mock_response = Mock()
        mock_response.json.return_value = MOCK_PRODUCT_RESPONSE
        mock_get.return_value = mock_response

        client = OpenFoodClient(cache=False)
        product = client.fetch_product("4099100207149")
        
        # Ensure the product is an instance of FoodProduct
        self.assertIsInstance(product, FoodProduct)
        
        # Check if the fetched data matches expected values
        self.assertEqual(product.product_name, "Rolled Oats")
        self.assertEqual(product.brands, ["millville", "aldi"])
        self.assertEqual(product.categories, [
            "plant-based-foods-and-beverages",
            "plant-based-foods",
            "breakfasts",
            "cereals-and-potatoes",
            "cereals-and-their-products",
            "breakfast-cereals",
            "flakes",
            "cereal-flakes",
            "rolled-flakes",
            "rolled-oats"
        ])
        self.assertEqual(product.image_url, "https://images.openfoodfacts.org/images/products/409/910/020/7149/front_en.3.400.jpg")
    
    @patch('requests.get')
    def test_fetch_product_not_found(self, mock_get):
        # Mock response for product not found
        mock_response = Mock()
        mock_response.json.return_value = {"status": 0}
        mock_get.return_value = mock_response

        client = OpenFoodClient()
        product = client.fetch_product("invalid_code")

        # Ensure that None is returned when the product is not found
        self.assertIsNone(product)

if __name__ == "__main__":
    unittest.main()
