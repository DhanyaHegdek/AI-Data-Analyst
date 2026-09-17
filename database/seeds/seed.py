from datetime import datetime, timedelta, timezone
from decimal import Decimal
import random

from sqlalchemy import delete
from sqlalchemy.orm import Session

from ai_data_analyst.database.connection import engine
from ai_data_analyst.models import (
    Category,
    Customer,
    Order,
    OrderItem,
    Payment,
    Product,
)


random.seed(42)


CUSTOMERS = [
    ("Isha Patel", "isha@example.com", "Bengaluru"),
    ("Aditya Joshi", "aditya@example.com", "Kolkata"),
    ("Rahul Sharma", "rahul@example.com", "Mumbai"),
    ("Priya Nair", "priya@example.com", "Kochi"),
    ("Arjun Reddy", "arjun@example.com", "Hyderabad"),
    ("Sneha Rao", "sneha@example.com", "Bengaluru"),
    ("Vikram Singh", "vikram@example.com", "Delhi"),
    ("Ananya Mehta", "ananya@example.com", "Pune"),
    ("Karan Shah", "karan@example.com", "Ahmedabad"),
    ("Neha Kapoor", "neha@example.com", "Jaipur"),
    ("Rohan Gupta", "rohan@example.com", "Chennai"),
    ("Kavya Iyer", "kavya@example.com", "Bengaluru"),
    ("Aman Verma", "aman@example.com", "Lucknow"),
    ("Pooja Desai", "pooja@example.com", "Mumbai"),
    ("Sanjay Kumar", "sanjay@example.com", "Delhi"),
    ("Meera Krishnan", "meera@example.com", "Chennai"),
    ("Nikhil Jain", "nikhil@example.com", "Pune"),
    ("Divya Menon", "divya@example.com", "Kochi"),
    ("Varun Malhotra", "varun@example.com", "Gurugram"),
    ("Aditi Rao", "aditi@example.com", "Mysuru"),
    ("Harish Bhat", "harish@example.com", "Mangaluru"),
    ("Swati Kulkarni", "swati@example.com", "Nagpur"),
    ("Manish Agarwal", "manish@example.com", "Noida"),
    ("Riya Sen", "riya@example.com", "Kolkata"),
    ("Deepak Patil", "deepak@example.com", "Bengaluru"),
]


CATEGORY_DATA = [
    ("Laptops", "Laptops and portable computers"),
    ("Mobiles", "Smartphones and mobile devices"),
    ("Cameras", "Digital cameras and photography equipment"),
    ("Televisions", "Smart televisions and displays"),
    ("Appliances", "Home and kitchen appliances"),
    ("Accessories", "Computer and mobile accessories"),
    ("Audio", "Headphones and audio equipment"),
    ("Gaming", "Gaming hardware and accessories"),
]


PRODUCT_DATA = [
    ("Gaming Laptop X", "Laptops", 145000),
    ("Laptop Air 13", "Laptops", 95000),
    ("Business Laptop Pro", "Laptops", 115000),
    ("Ultrabook Z", "Laptops", 125000),
    ("Budget Laptop 15", "Laptops", 55000),

    ("Smartphone Pro Max", "Mobiles", 85000),
    ("Smartphone Ultra", "Mobiles", 72000),
    ("Smartphone Lite", "Mobiles", 28000),
    ("Android Max 5G", "Mobiles", 45000),
    ("Foldable Phone X", "Mobiles", 110000),

    ("Digital Camera", "Cameras", 68000),
    ("Mirrorless Camera Pro", "Cameras", 125000),
    ("Action Camera 4K", "Cameras", 32000),
    ("Camera Lens 50mm", "Cameras", 42000),
    ("Camera Lens 85mm", "Cameras", 58000),

    ("4K Smart TV 55", "Televisions", 75000),
    ("4K Smart TV 65", "Televisions", 105000),
    ("OLED TV 55", "Televisions", 135000),
    ("LED TV 43", "Televisions", 48000),
    ("Mini LED TV", "Televisions", 98000),

    ("Air Conditioner", "Appliances", 62000),
    ("Refrigerator", "Appliances", 68000),
    ("Washing Machine", "Appliances", 54000),
    ("Microwave Oven", "Appliances", 18000),
    ("Dishwasher", "Appliances", 72000),

    ("Wireless Keyboard", "Accessories", 3500),
    ("Mechanical Keyboard", "Accessories", 7500),
    ("Wireless Mouse", "Accessories", 2200),
    ("USB-C Hub", "Accessories", 4500),
    ("Laptop Backpack", "Accessories", 3200),

    ("Wireless Headphones", "Audio", 12000),
    ("Noise Cancelling Headphones", "Audio", 22000),
    ("Bluetooth Speaker", "Audio", 8500),
    ("Premium Earbuds", "Audio", 15000),
    ("Studio Headphones", "Audio", 18000),

    ("Gaming Monitor", "Gaming", 32000),
    ("Gaming Keyboard", "Gaming", 9000),
    ("Gaming Mouse", "Gaming", 5500),
    ("Gaming Headset", "Gaming", 7500),
    ("Gaming Console", "Gaming", 55000),
]


def main():
    with Session(engine) as session:
        # Clear business data so the seed is repeatable.
        session.execute(delete(Payment))
        session.execute(delete(OrderItem))
        session.execute(delete(Order))
        session.execute(delete(Product))
        session.execute(delete(Category))
        session.execute(delete(Customer))

        # -------------------------
        # Customers
        # -------------------------
        customers = [
            Customer(
                name=name,
                email=email,
                city=city,
            )
            for name, email, city in CUSTOMERS
        ]

        session.add_all(customers)
        session.flush()

        # -------------------------
        # Categories
        # -------------------------
        categories = {
            name: Category(
                name=name,
                description=description,
            )
            for name, description in CATEGORY_DATA
        }

        session.add_all(categories.values())
        session.flush()

        # -------------------------
        # Products
        # -------------------------
        products = []

        for name, category_name, price in PRODUCT_DATA:
            product = Product(
                name=name,
                category_id=categories[category_name].id,
                price=Decimal(str(price)),
            )
            products.append(product)

        session.add_all(products)
        session.flush()

        # -------------------------
        # Orders
        # -------------------------
        statuses = [
            "completed",
            "completed",
            "completed",
            "shipped",
            "processing",
            "cancelled",
        ]

        orders = []

        start_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2026, 9, 17, tzinfo=timezone.utc)

        date_range = (end_date - start_date).days

        for _ in range(150):
            customer = random.choice(customers)

            order_date = start_date + timedelta(
                days=random.randint(0, date_range),
                hours=random.randint(8, 20),
                minutes=random.randint(0, 59),
            )

            order = Order(
                customer_id=customer.id,
                order_date=order_date,
                total_amount=Decimal("0.00"),
                status=random.choice(statuses),
            )

            orders.append(order)

        session.add_all(orders)
        session.flush()

        # -------------------------
        # Order Items
        # -------------------------
        for order in orders:
            item_count = random.randint(1, 4)
            selected_products = random.sample(products, item_count)

            total = Decimal("0.00")

            for product in selected_products:
                quantity = random.randint(1, 5)

                unit_price = Decimal(product.price)

                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                )

                session.add(item)

                total += unit_price * quantity

            order.total_amount = total

        session.flush()

        # -------------------------
        # Payments
        # -------------------------
        for order in orders:
            payment_status = (
                "completed"
                if order.status != "cancelled"
                else "refunded"
            )

            payment = Payment(
                order_id=order.id,
                payment_date=order.order_date + timedelta(
                    minutes=random.randint(5, 180)
                ),
                amount=order.total_amount,
                status=payment_status,
            )

            session.add(payment)

        session.commit()

        print("✅ Seed completed successfully!")
        print(f"Customers: {len(customers)}")
        print(f"Categories: {len(categories)}")
        print(f"Products: {len(products)}")
        print(f"Orders: {len(orders)}")


if __name__ == "__main__":
    main()