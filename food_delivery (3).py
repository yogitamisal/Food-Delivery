# Paste the completed class definitions here.
#1. user
from abc import ABC, abstractmethod

class User(ABC):

    def __init__(self, name, phone):
        self._name = name
        self._phone = phone
        self._wallet_balance = 0

    def add_to_wallet(self, amount):
        if amount >= 0:
          self._wallet_balance += amount

    @abstractmethod
    def notify(self, message):
        pass

    @abstractmethod
    def display_profile(self):
        pass


# 2 customer
class Customer(User):

    def __init__(self, name, phone, address):
       super().__init__(name,phone)
       self.address = address
       self.order_history = []

    def notify(self, message):
        print("Notificatoin: ",message)

    def display_profile(self):
        print("Name: ", self._name)
        print("Phone: ", self._phone)
        print("Wallet Balance: ", self._wallet_balance)
        print("Address: ", self.address)

    def place_order(self, restaurant, items):
        order = Order(items)
        self.order_history.append(order)
        print("Your OTP is: ",order._otp)

        return order

# delivery 
class DeliveryPartner(User):

    def init(self, name, phone, vehicle):

        super().__init__(name,phone)

        self.vehicle = vehicle

        self.is_available = True

        self.rating = 0.0

    def notify(self, message):

        self.message = message

        print("Notification: ", message, "for delivery partner: ", self._name)

    def display_profile(self):

        print("Name: ", self._name)

        print("Phone: ", self._phone)

        print("availibility: ", self.is_available)

        print("Rating: ", self.rating)

    def accept_order(self, order):

        order.update_status("Accepted")

        self.is_available = False

    def deliver(self, order, otp):

      if order.verify_otp(otp):
        order.update_status("Delivered")
        self.is_available = True


# 4 . menuitem
class MenuItem:

    def __init__(self, name, price, is_veg):
        self.name = name
        self.price = price
        self.is_veg = is_veg

# 5. Restaurant
class Restaurant:

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self._menu = []

    def add_item(self, menu_item):
        self._menu.append(menu_item)

    def get_menu(self):
        return self._menu

    def is_open(self):
        return True

# 6 Ordeom

import random

class Order:

    _counter = 1

    def __init__(self, items):
        self._order_id = Order._counter
        Order._counter += 1
        self._items = items
        self._status = "Placed"
        self._otp = random.randint(1000,9999)



    def calculate_bill(self):
        subtotal = 0
        for item in self._items:
          subtotal += item.price

        gst = subtotal * 0.05
        packaging_fees = 20

        total = subtotal + gst + packaging_fees

        return total

    def estimated_time(self):
        return 30

    def update_status(self, new_status):
      if new_status in ['Placed','Order Accepted','Processing','Cancelled','Delivered']:
        self._status = new_status

    def verify_otp(self, otp):
      if otp == self._otp:
        return True
      else:
        return False
