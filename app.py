import streamlit as st

# Import classes from your OOP file
# Rename "food_delivery (3).py" to "food_delivery.py" for easier importing.
from food_delivery import Customer, Restaurant, MenuItem, Order, DeliveryPartner


st.set_page_config(
    page_title="Food Delivery System",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Food Delivery System")
st.write("Simple Streamlit interface for the OOP Food Delivery Project")

# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "restaurant" not in st.session_state:
    # Demo restaurant and menu
    restaurant = Restaurant("Food Corner", "Aurangabad")
    restaurant.add_item(MenuItem("Biryani", 250, False))
    restaurant.add_item(MenuItem("Kebab", 180, False))
    restaurant.add_item(MenuItem("Paneer Tikka", 200, True))
    restaurant.add_item(MenuItem("Veg Biryani", 180, True))
    st.session_state.restaurant = restaurant

if "order" not in st.session_state:
    st.session_state.order = None

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = None


# ---------------------------------------------------------
# 1. Create Customer
# ---------------------------------------------------------
st.header("1️⃣ Create Customer")

with st.form("customer_form"):
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    address = st.text_input("Delivery Address")

    create_customer = st.form_submit_button("Create Customer")

    if create_customer:
        if name and phone and address:
            st.session_state.customer = Customer(name, phone, address)
            st.success(f"Customer '{name}' created successfully!")
        else:
            st.warning("Please enter all customer details.")


# Show customer information
if st.session_state.customer:
    customer = st.session_state.customer

    st.subheader("Customer Profile")
    st.write("**Name:**", customer._name)
    st.write("**Phone:**", customer._phone)
    st.write("**Address:**", customer.address)
    st.write("**Wallet Balance:** ₹", customer._wallet_balance)


# ---------------------------------------------------------
# 2. Add Wallet Balance
# ---------------------------------------------------------
st.header("2️⃣ Add Wallet Balance")

if st.session_state.customer:
    amount = st.number_input(
        "Enter amount to add (₹)",
        min_value=0.0,
        value=100.0,
        step=50.0
    )

    if st.button("Add Money"):
        if amount > 0:
            st.session_state.customer.add_to_wallet(amount)
            st.success(f"₹{amount:.2f} added to wallet.")
            st.write(
                f"Current Wallet Balance: "
                f"₹{st.session_state.customer._wallet_balance:.2f}"
            )
        else:
            st.warning("Enter an amount greater than 0.")
else:
    st.info("First create a customer.")


# ---------------------------------------------------------
# 3. Show Restaurant Menu
# ---------------------------------------------------------
st.header("3️⃣ Restaurant Menu")

restaurant = st.session_state.restaurant

st.write(f"### {restaurant.name}")
st.write(f"Location: {restaurant.location}")

menu = restaurant.get_menu()

for i, item in enumerate(menu):
    veg = "🌱 Veg" if item.is_veg else "🍗 Non-Veg"

    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.write(f"**{item.name}**")
    with col2:
        st.write(f"₹{item.price}")
    with col3:
        st.write(veg)


# ---------------------------------------------------------
# 4. Place an Order
# ---------------------------------------------------------
st.header("4️⃣ Place an Order")

if st.session_state.customer:

    item_names = [
        f"{item.name} - ₹{item.price}"
        for item in menu
    ]

    selected_items = st.multiselect(
        "Select food items",
        item_names
    )

    if st.button("Place Order"):

        if not selected_items:
            st.warning("Please select at least one item.")
        else:
            selected_objects = []

            for selected in selected_items:
                for item in menu:
                    if selected == f"{item.name} - ₹{item.price}":
                        selected_objects.append(item)
                        break

            order = st.session_state.customer.place_order(
                restaurant,
                selected_objects
            )

            st.session_state.order = order

            st.success(
                f"Order #{order._order_id} placed successfully!"
            )

            st.info(f"Your delivery OTP is: {order._otp}")

            st.write(
                f"**Bill:** ₹{order.calculate_bill():.2f}"
            )

            st.write(
                f"**Estimated Time:** "
                f"{order.estimated_time()} minutes"
            )

else:
    st.info("Create a customer before placing an order.")


# ---------------------------------------------------------
# Show Order Details
# ---------------------------------------------------------
if st.session_state.order:

    order = st.session_state.order

    st.subheader("📦 Current Order")

    st.write("**Order ID:**", order._order_id)
    st.write("**Status:**", order._status)
    st.write("**Bill:** ₹", f"{order.calculate_bill():.2f}")
    st.write("**Estimated Time:**", f"{order.estimated_time()} minutes")


# ---------------------------------------------------------
# 5. Create Delivery Partner
# ---------------------------------------------------------
st.header("5️⃣ Create Delivery Partner")

with st.form("delivery_form"):

    delivery_name = st.text_input("Delivery Partner Name")
    delivery_phone = st.text_input("Delivery Partner Phone")
    vehicle = st.selectbox(
        "Vehicle",
        ["Bike", "Scooter", "Cycle"]
    )

    create_partner = st.form_submit_button(
        "Create Delivery Partner"
    )

    if create_partner:

        if delivery_name and delivery_phone:

            # Your uploaded class has "init" instead of "__init__".
            # Therefore create the object and initialize its attributes here.
            partner = DeliveryPartner.__new__(DeliveryPartner)

            partner._name = delivery_name
            partner._phone = delivery_phone
            partner._wallet_balance = 0
            partner.vehicle = vehicle
            partner.is_available = True
            partner.rating = 0.0

            st.session_state.delivery_partner = partner

            st.success(
                f"Delivery Partner '{delivery_name}' created successfully!"
            )

        else:
            st.warning("Please enter name and phone.")


# ---------------------------------------------------------
# 6. Accept Order
# ---------------------------------------------------------
st.header("6️⃣ Accept Order")

if st.session_state.order and st.session_state.delivery_partner:

    order = st.session_state.order
    partner = st.session_state.delivery_partner

    st.write("**Order Status:**", order._status)
    st.write("**Partner Available:**", partner.is_available)

    if st.button("Accept Order"):

        if partner.is_available and order._status == "Placed":

            partner.accept_order(order)

            # Your Order.update_status() does not allow "Accepted".
            # It expects "Order Accepted".
            # So correct the status for the current class definition.
            order._status = "Order Accepted"

            st.success(
                f"Order #{order._order_id} accepted by "
                f"{partner._name}."
            )

        else:
            st.warning(
                "Order cannot be accepted. "
                "Check order status or partner availability."
            )

else:
    st.info("Create an order and delivery partner first.")


# ---------------------------------------------------------
# 7. Enter OTP and Complete Delivery
# ---------------------------------------------------------
st.header("7️⃣ Complete Delivery")

if st.session_state.order and st.session_state.delivery_partner:

    order = st.session_state.order
    partner = st.session_state.delivery_partner

    st.write("**Current Order Status:**", order._status)

    otp = st.number_input(
        "Enter Delivery OTP",
        min_value=1000,
        max_value=9999,
        value=1000,
        step=1
    )

    if st.button("Verify OTP & Complete Delivery"):

        if order.verify_otp(int(otp)):

            partner.deliver(order, int(otp))

            # Ensure final status is displayed correctly
            order._status = "Delivered"

            st.success(
                f"🎉 Order #{order._order_id} delivered successfully!"
            )

            st.write("**Final Status:** Delivered")
            st.write(
                f"**Delivery Partner:** {partner._name}"
            )

        else:
            st.error("❌ Invalid OTP. Delivery not completed.")

else:
    st.info("Create an order and delivery partner first.")


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.divider()
st.caption("OOP Food Delivery System | Streamlit Interface")
