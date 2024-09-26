import unittest
from shelfaware.food_inventory.models import get_engine, Base, User, List, Category, ListItem, FoodItem
from shelfaware.food_inventory.inventory import InventoryManager
from sqlalchemy.orm import sessionmaker

class TestInventoryManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Setup an in-memory SQLite database for testing
        cls.engine = get_engine()
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.manager = InventoryManager()

    def setUp(self):
        # Start a new session before each test
        self.session = self.Session()

    def tearDown(self):
        # Rollback any changes made during tests to keep the tests isolated
        self.session.rollback()

    @classmethod
    def tearDownClass(cls):
        # Drop the tables after all tests are completed
        Base.metadata.drop_all(cls.engine)

    def test_add_user(self):
        self.manager.add_user("test_user")
        user = self.session.query(User).filter_by(username="test_user").first()
        self.assertIsNotNone(user, "User should be added")

    def test_add_list(self):
        self.manager.add_user("test_user2")
        self.manager.add_list("test_user2", "Inventory")
        
        user = self.session.query(User).filter_by(username="test_user2").first()
        user_list = self.session.query(List).filter_by(name="Inventory", user=user).first()

        self.assertIsNotNone(user_list, "List should be added for the user")

    def test_add_category(self):
        self.manager.add_category("Produce")
        category = self.session.query(Category).filter_by(name="Produce").first()
        self.assertIsNotNone(category, "Category should be added")

    def test_add_list_item(self):
        self.manager.add_user("test_user3")
        self.manager.add_list("test_user3", "Shopping List")
        self.manager.add_category("Produce")
        self.manager.add_list_item("test_user3", "Shopping List", "Carrot", 5, "Produce")

        user = self.session.query(User).filter_by(username="test_user3").first()
        user_list = self.session.query(List).filter_by(name="Shopping List", user=user).first()
        list_item = self.session.query(ListItem).filter_by(name="Carrot").first()

        self.assertIsNotNone(list_item, "ListItem should be added")
        self.assertEqual(list_item.list.name, "Shopping List", "Item should belong to the correct list")
        self.assertEqual(list_item.quantity, 5, "Item should have the correct quantity")

    def test_get_user_lists(self):
        self.manager.add_user("test_user4")
        self.manager.add_list("test_user4", "Shopping List")
        self.manager.add_list("test_user4", "Inventory")

        lists = self.manager.get_user_lists("test_user4")
        self.assertIn("Shopping List", lists, "User should have 'Shopping List'")
        self.assertIn("Inventory", lists, "User should have 'Inventory'")

    def test_update_quantity(self):
        self.manager.add_user("test_user5")
        self.manager.add_list("test_user5", "Inventory")
        self.manager.add_category("Produce")
        self.manager.add_list_item("test_user5", "Inventory", "Apple", 3, "Produce")

        # Update quantity
        self.manager.update_quantity("Inventory", "Apple", 5)
        list_item = self.session.query(ListItem).filter_by(name="Apple").first()

        self.assertEqual(list_item.quantity, 5, "Item quantity should be updated")

    def test_remove_list_item(self):
        self.manager.add_user("test_user6")
        self.manager.add_list("test_user6", "Shopping List")
        self.manager.add_category("Produce")
        self.manager.add_list_item("test_user6", "Shopping List", "Banana", 2, "Produce")

        # Remove list item
        self.manager.remove_list_item("Shopping List", "Banana")
        list_item = self.session.query(ListItem).filter_by(name="Banana").first()

        self.assertIsNotNone(list_item.date_removed, "ListItem should be marked as removed")

    def test_add_action(self):
        self.manager.add_user("test_user7")
        self.manager.add_list("test_user7", "Inventory")
        self.manager.add_category("Meat")
        self.manager.add_list_item("test_user7", "Inventory", "Chicken", 2, "Meat")

        # Add an action for the item
        self.manager.add_action("test_user7", "Chicken", "purchase", 2)

        user = self.session.query(User).filter_by(username="test_user7").first()
        list_item = self.session.query(ListItem).filter_by(name="Chicken").first()

        self.assertIsNotNone(user, "User should exist for the action")
        self.assertIsNotNone(list_item, "ListItem should exist for the action")

if __name__ == '__main__':
    unittest.main()
