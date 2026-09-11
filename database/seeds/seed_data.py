import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ai_data_analyst.models import (
    Category,
    Customer,
    Order,
    OrderItem,
    Payment,
)
from ai_data_analyst.models.product import Product

from dotenv import load_dotenv
import os


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set.")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

random.seed(42)


# ---------------------------------------------------------
# Sample business data
# ---------------------------------------------------------

CATEGORIES = [
    ("Electronics", "Electronic devices and accessories"),
    ("Computers", "Laptops, desktops and computer accessories"),
    ("Mobile", "Smartphones and mobile accessories"),
    ("Home Appliances", "Appliances and household electronics"),
    ("Furniture", "Furniture and home office products"),
    ("Fashion", "Clothing and fashion products"),
    ("Sports", "Sports and fitness products"),
    ("Books", "Books and educational materials"),
]

PRODUCTS = [
    ("Laptop Pro 14", "Computers", 85000),
    ("Laptop Air 13", "Computers", 68000),
    ("Gaming Laptop X", "Computers", 125000),
    ("Mechanical Keyboard", "Computers", 6500),
    ("Wireless Mouse", "Computers", 1800),
    ("4K Monitor", "Computers", 32000),
    ("USB-C Hub", "Computers", 3500),
    ("External SSD 1TB", "Computers", 8500),

    ("Smartphone Pro", "Mobile", 72000),
    ("Smartphone Lite", "Mobile", 28000),
    ("Smartphone Ultra", "Mobile", 95000),
    ("Wireless Earbuds", "Mobile", 5500),
    ("Fast Charger", "Mobile", 2200),
    ("Phone Case", "Mobile", 900),
    ("Power Bank", "Mobile", 2800),

    ("Smart TV 55", "Electronics", 52000),
    ("Bluetooth Speaker", "Electronics", 4500),
    ("Digital Camera", "Electronics", 68000),
    ("Action Camera", "Electronics", 24000),
    ("Smart Watch", "Electronics", 12000),

    ("Air Conditioner", "Home Appliances", 48000),
    ("Refrigerator", "Home Appliances", 62000),
    ("Washing Machine", "Home Appliances", 42000),
    ("Microwave Oven", "Home Appliances", 15000),
    ("Air Purifier", "Home Appliances", 18000),

    ("Office Chair", "Furniture", 14000),
    ("Study Table", "Furniture", 12000),
    ("Bookshelf", "Furniture", 9500),
    ("Standing Desk", "Furniture", 28000),
    ("Coffee Table", "Furniture", 8500),

    ("Running Shoes", "Sports", 6500),
    ("Yoga Mat", "Sports", 1800),
    ("Dumbbell Set", "Sports", 5500),
    ("Tennis Racket", "Sports", 8500),
    ("Fitness Tracker", "Sports", 4500),

    ("Men's T-Shirt", "Fashion", 1200),
    ("Women's Jacket", "Fashion", 4500),
    ("Running Jacket", "Fashion", 3800),
    ("Backpack", "Fashion", 2500),
    ("Sneakers", "Fashion", 5200),

    ("Python Programming", "Books", 1200),
    ("Data Science Handbook", "Books", 1800),
    ("AI Engineering", "Books", 2200),
    ("SQL Mastery", "Books", 1400),
    ("Machine Learning Guide", "Books", 2000),
]

CITIES = [
    "Bengaluru",
    "Mumbai",
    "Delhi",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Kochi",
]

FIRST_NAMES = [
    "Aarav",
    "Arjun",
    "Rahul",
    "Vikram",
    "Rohan",
    "Aditya",
    "Karan",
    "Neha",
    "Ananya",
    "Priya",
    "Sneha",
    "Kavya",
    "Meera",
    "Pooja",
    "Divya",
    "Isha",
    "Nisha",
    "Aditi",
]

LAST_NAMES = [
    "Sharma",
    "Patel",
    "Reddy",
    "Kumar",
    "Singh",
    "Mehta",
    "Nair",
    "Rao",
    "Iyer",
    "Gupta",
    "Joshi",
    "Verma",
]


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def random_date():
    """
    Generate dates between January 1, 2025
    and September 1, 2026.
    """

    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 9, 1, tzinfo=timezone.utc)

    days = (end - start).days

    return start + timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


# ---------------------------------------------------------
# Seed database
# ---------------------------------------------------------

def seed_database():

    with Session(engine) as session:

        print("Clearing existing business data...")

        session.query(Payment).delete()
        session.query(OrderItem).delete()
        session.query(Order).delete()
        session.query(Product).delete()
        session.query(Category).delete()
        session.query(Customer).delete()

        session.commit()

        # -------------------------------------------------
        # Categories
        # -------------------------------------------------

        print("Creating categories...")

        category_objects = {}

        for name, description in CATEGORIES:

            category = Category(
                name=name,
                description=description,
            )

            session.add(category)
            category_objects[name] = category

        session.flush()

        # -------------------------------------------------
        # Products
        # -------------------------------------------------

        print("Creating products...")

        product_objects = []

        for name, category_name, price in PRODUCTS:

            product = Product(
                name=name,
                category=category_objects[category_name],
                price=Decimal(str(price)),
                created_at=random_date(),
            )

            session.add(product)
            product_objects.append(product)

        session.flush()

        # -------------------------------------------------
        # Customers
        # -------------------------------------------------

        print("Creating customers...")

        customer_objects = []

        for i in range(1, 101):

            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)

            customer = Customer(
                name=f"{first_name} {last_name}",
                email=f"customer{i}@example.com",
                city=random.choice(CITIES),
                created_at=random_date(),
            )

            session.add(customer)
            customer_objects.append(customer)

        session.flush()

        # -------------------------------------------------
        # Orders
        # -------------------------------------------------

        print("Creating orders...")

        order_statuses = [
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
        ]

        for order_number in range(1, 501):

            customer = random.choice(customer_objects)

            order_date = random_date()

            status = random.choices(
                order_statuses,
                weights=[5, 10, 15, 65, 5],
                k=1,
            )[0]

            order = Order(
                customer=customer,
                order_date=order_date,
                total_amount=Decimal("0.00"),
                status=status,
            )

            session.add(order)
            session.flush()

            # -------------------------------------------------
            # Order Items
            # -------------------------------------------------

            number_of_items = random.randint(1, 5)

            selected_products = random.sample(
                product_objects,
                number_of_items,
            )

            total_amount = Decimal("0.00")

            for product in selected_products:

                quantity = random.randint(1, 4)

                unit_price = Decimal(str(product.price))

                item_total = unit_price * quantity

                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                )

                session.add(order_item)

                total_amount += item_total

            order.total_amount = total_amount

            # -------------------------------------------------
            # Payment
            # -------------------------------------------------

            if status != "cancelled":

                payment_status = random.choices(
                    ["completed", "pending", "failed"],
                    weights=[90, 7, 3],
                    k=1,
                )[0]

                payment = Payment(
                    order=order,
                    payment_date=order_date + timedelta(
                        hours=random.randint(1, 48)
                    ),
                    amount=total_amount,
                    status=payment_status,
                )

                session.add(payment)

        session.commit()

        print()
        print("✅ Database seeding completed!")
        print()

        print(f"Categories : {session.query(Category).count()}")
        print(f"Products   : {session.query(Product).count()}")
        print(f"Customers  : {session.query(Customer).count()}")
        print(f"Orders     : {session.query(Order).count()}")
        print(f"OrderItems : {session.query(OrderItem).count()}")
        print(f"Payments   : {session.query(Payment).count()}")


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    seed_database()