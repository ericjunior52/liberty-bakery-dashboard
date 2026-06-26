import sqlite3
from datetime import datetime


DATABASE_NAME = "bakery.db"


def connect_to_database():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            order_date TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def seed_starting_products():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    if product_count == 0:
        starting_products = [
            ("Butter Bread", "Bread", 3.50, 25),
            ("Sugar Bread", "Bread", 3.00, 18),
            ("Tea Bread", "Bread", 2.75, 12),
            ("Wheat/Brown Bread", "Bread", 4.00, 20),
        ]

        cursor.executemany(
            """
            INSERT INTO products (product, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            starting_products,
        )

    connection.commit()
    connection.close()


def add_product(product, category, price, stock):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products (product, category, price, stock)
        VALUES (?, ?, ?, ?)
        """,
        (product, category, price, stock),
    )

    connection.commit()
    connection.close()


def get_products():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, product, category, price, stock
        FROM products
        ORDER BY id DESC
        """
    )

    products = cursor.fetchall()
    connection.close()

    return products


def add_order(customer_name, product, quantity, total):
    connection = connect_to_database()
    cursor = connection.cursor()

    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO orders (customer_name, product, quantity, total, order_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (customer_name, product, quantity, total, order_date),
    )

    connection.commit()
    connection.close()


def reduce_product_stock(product_id, quantity):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE products
        SET stock = stock - ?
        WHERE id = ?
        """,
        (quantity, product_id),
    )

    connection.commit()
    connection.close()


def get_orders():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, customer_name, product, quantity, total, order_date
        FROM orders
        ORDER BY id DESC
        """
    )

    orders = cursor.fetchall()
    connection.close()

    return orders


def get_total_sales():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT SUM(total) FROM orders")
    total_sales = cursor.fetchone()[0]

    connection.close()

    if total_sales is None:
        return 0

    return total_sales