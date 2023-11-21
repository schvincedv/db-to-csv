import sqlite3
from Classes.DatabaseHandlers.DatabaseEventHandlers import logging
import sys

TEST_DB_PATH = f'{sys.path[1]}\\databases\\example.db'


class DatabaseCreator:
    @staticmethod
    def create_random_db() -> str:
        try:
            sql_conn = sqlite3.connect(TEST_DB_PATH)

            sql_conn.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL
                        )
                    ''')

            sql_conn.execute(
                "INSERT INTO users (name, email) VALUES ('Saul Hudson', 'a#minor4ever@songingernogre.com.uk.eu')")
            sql_conn.execute("INSERT INTO users (name, email) VALUES ('Example 2', 'e2@citromail.hu')")

            sql_conn.execute('''
                        CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            product TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id)
                        )
                    ''')

            sql_conn.execute("INSERT INTO orders (user_id, product, quantity)"
                             "VALUES (1, 'Product A Type Les Paul Rec Reiusse 59', 3)")

            sql_conn.execute("INSERT INTO orders (user_id, product, quantity)"
                             "VALUES (2, 'Product B Type Marshall Rec JCM800 86', 2)")

            sql_conn.commit()
            sql_conn.close()

            return TEST_DB_PATH
        except Exception as e:
            logging.error(f"Error creating random database: {e}")
            raise
