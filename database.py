import sqlite3


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
        ]

        cursor.executemany(
            """
            INSERT INTO products (product, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            starting_products
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
        (product, category, price, stock)
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