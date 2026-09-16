BUSINESS_SCHEMA = """
PostgreSQL business database schema:

TABLE customers
- id: integer, primary key
- name: varchar
- email: varchar, unique
- city: varchar, nullable
- created_at: timestamp with timezone

TABLE categories
- id: integer, primary key
- name: varchar, unique
- description: text, nullable

TABLE products
- id: integer, primary key
- name: varchar
- category_id: integer, foreign key -> categories.id
- price: numeric(12,2)
- created_at: timestamp with timezone

TABLE orders
- id: integer, primary key
- customer_id: integer, foreign key -> customers.id
- order_date: timestamp with timezone
- total_amount: numeric(12,2)
- status: varchar

TABLE order_items
- id: integer, primary key
- order_id: integer, foreign key -> orders.id
- product_id: integer, foreign key -> products.id
- quantity: integer
- unit_price: numeric(12,2)

TABLE payments
- id: integer, primary key
- order_id: integer, foreign key -> orders.id
- payment_date: timestamp with timezone
- amount: numeric(12,2)
- status: varchar

RELATIONSHIPS
- customers.id -> orders.customer_id
- categories.id -> products.category_id
- orders.id -> order_items.order_id
- products.id -> order_items.product_id
- orders.id -> payments.order_id
"""