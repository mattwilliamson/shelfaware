import datetime
from sqlalchemy.orm import sessionmaker
from shelfaware.food_inventory.models import User, List, Category, ListItem, FoodItem, Action, get_engine

class InventoryManager:
    def __init__(self):
        self.engine = get_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_user(self, username):
        user = User(username=username)
        self.session.add(user)
        self.session.commit()

    def add_list(self, username, list_name):
        user = self.session.query(User).filter_by(username=username).first()
        if not user:
            raise ValueError(f"User {username} not found.")
        
        user_list = List(name=list_name, user=user)
        self.session.add(user_list)
        self.session.commit()

    def add_category(self, category_name):
        # Check if category already exists
        existing_category = self.session.query(Category).filter_by(name=category_name).first()
        if not existing_category:
            category = Category(name=category_name)
            self.session.add(category)
            self.session.commit()


    def add_list_item(self, username, list_name, item_name, quantity, category_name, food_name=None):
        user = self.session.query(User).filter_by(username=username).first()
        user_list = self.session.query(List).filter_by(name=list_name, user=user).first()
        category = self.session.query(Category).filter_by(name=category_name).first()
        food = self.session.query(FoodItem).filter_by(name=food_name).first() if food_name else None
        
        if not user_list:
            raise ValueError(f"List {list_name} not found for user {username}.")
        if not category:
            raise ValueError(f"Category {category_name} not found.")
        
        list_item = ListItem(
            name=item_name,
            quantity=quantity,
            list=user_list,
            category=category,
            food=food
        )
        self.session.add(list_item)
        self.session.commit()

    def get_user_lists(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            return [user_list.name for user_list in user.lists]
        return []

    def get_list_items(self, username, list_name):
        user = self.session.query(User).filter_by(username=username).first()
        user_list = self.session.query(List).filter_by(name=list_name, user=user).first()
        if user_list:
            return [list_item.name for list_item in user_list.list_items]
        return []

    def update_quantity(self, list_name, item_name, quantity):
        list_item = self.session.query(ListItem).filter_by(name=item_name).first()
        if list_item and list_item.list.name == list_name:
            list_item.quantity = quantity
            self.session.commit()
    
    def remove_list_item(self, list_name, item_name):
        list_item = self.session.query(ListItem).filter_by(name=item_name).first()
        if list_item and list_item.list.name == list_name:
            list_item.date_removed = datetime.datetime.utcnow()  # Mark as removed
            self.session.commit()

    def add_action(self, username, item_name, action_type, quantity=1.0):
        user = self.session.query(User).filter_by(username=username).first()
        list_item = self.session.query(ListItem).filter_by(name=item_name).first()

        if not user:
            raise ValueError(f"User {username} not found.")
        if not list_item:
            raise ValueError(f"ListItem {item_name} not found.")

        action = Action(action_type=action_type, quantity=quantity, user=user, list_item=list_item)
        self.session.add(action)
        self.session.commit()
