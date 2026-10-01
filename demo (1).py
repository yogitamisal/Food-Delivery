# demo.py
# Demo program for the OOP Food Delivery Project

from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem


# 1. Register customer Priya
priya = Customer("Priya", "9876543210", "Bangalore")

print("=== CUSTOMER REGISTERED ===")
priya.display_profile()


# 2. Register delivery partner Rajesh with Bike
# The current food_delivery.py has init() instead of __init__(),
# so we initialize the object manually for this demo.
rajesh = DeliveryPartner.__new__(DeliveryPartner)
rajesh._name = "Rajesh"
rajesh._phone = "0000000000"
rajesh._wallet_balance = 0
rajesh.vehicle = "Bike"
rajesh.is_available = True
rajesh.rating = 0.0

print("\n=== DELIVERY PARTNER REGISTERED ===")
rajesh.display_profile()


# 3. Create Bawarchi at MG Road and add Biryani and Kebab
bawarchi = Restaurant("Bawarchi", "MG Road")

biryani = MenuItem("Biryani", 250, False)
kebab = MenuItem("Kebab", 180, False)

bawarchi.add_item(biryani)
bawarchi.add_item(kebab)

print("\n=== RESTAURANT MENU ===")
print(bawarchi.name, "-", bawarchi.location)

for item in bawarchi.get_menu():
    print(item.name, "₹", item.price)


# 4. Top up Priya's wallet by 500, then attempt -100
print("\n=== WALLET ===")

priya.add_to_wallet(500)
print("After adding ₹500:")
print("Wallet Balance:", priya._wallet_balance)

priya.add_to_wallet(-100)
print("After attempting to add -₹100:")
print("Wallet Balance:", priya._wallet_balance)


# 5. Priya places an order for Biryani and Kebab
print("\n=== PLACE ORDER ===")

order = priya.place_order(bawarchi, [biryani, kebab])


# 6. Print subtotal, GST, packaging fee, total and estimated time
print("\n=== ORDER DETAILS ===")

subtotal = 0
for item in order._items:
    subtotal += item.price

gst = subtotal * 0.05
packaging_fee = 20
total = order.calculate_bill()

print("Order ID:", order._order_id)
print("Subtotal: ₹", subtotal)
print("GST (5%): ₹", gst)
print("Packaging Fee: ₹", packaging_fee)
print("Total: ₹", total)
print("Estimated Delivery Time:", order.estimated_time(), "minutes")


# 7. Rajesh accepts the order
print("\n=== DELIVERY ===")

rajesh.accept_order(order)

# In the current class, update_status() does not allow "Accepted";
# it allows "Order Accepted".
order._status = "Order Accepted"

print("Order Status:", order._status)
print("Rajesh accepted the order.")


# Try a wrong OTP
wrong_otp = 9999

print("\nTrying wrong OTP:", wrong_otp)

if not order.verify_otp(wrong_otp):
    print("Wrong OTP. Delivery not completed.")


# Deliver using OTP 1234
# The Order class generates a random OTP, so set it to 1234
# to match the requested demo scenario.
order._otp = 1234

correct_otp = 1234

print("Trying correct OTP:", correct_otp)

rajesh.deliver(order, correct_otp)

print("Order Status:", order._status)


# 8. Notify Priya and Rajesh
print("\n=== NOTIFICATIONS ===")

priya.notify("Order delivered")
rajesh.notify("Order delivered")

print("\n=== DEMO COMPLETED ===")
