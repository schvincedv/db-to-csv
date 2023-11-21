import configparser
import sys
import sqlite3
import logging
from typing import Optional
import pandas as pd

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'{sys.path[1]}\\logs\\error_logs_v1x.log')
    ]
)


class DatabaseConnector:
    def __init__(self, database_file: str = None, config_file: str = "config.ini") -> None:
        """
        Initialize a DatabaseConnector instance.

        Parameters:
        - database_file (str): The path to the SQLite database file.
        - config_file (str): The path to the configuration file.
        """
        self.database_file = database_file
        self.config_file = config_file
        self.connection = None

    def connect(self) -> sqlite3.Connection:
        """
        Connect to the SQLite database.

        Returns:
        - sqlite3.Connection: The SQLite database connection object.
        """
        try:
            self.connection = sqlite3.connect(self.database_file)
            return self.connection
        except sqlite3.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def read_config_file(self) -> configparser.SectionProxy:
        """
        Read the configuration file and return the 'Database' section.

        Returns:
        - configparser.SectionProxy: The 'Database' section of the configuration file.
        """
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            return config['Database']
        except configparser.Error as e:
            logging.error(f"Error reading config file: {e}")
            raise

    def execute_query(self, query: str, data: Optional[tuple] = None) -> sqlite3.Cursor:
        """
        Execute an SQL query on the connected database.

        Parameters:
        - query (str): The SQL query to execute.
        - data (Optional[tuple]): The data to be used in the query if applicable.

        Returns:
        - sqlite3.Cursor: The SQLite database cursor object.
        """
        try:
            cursor = self.connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            return cursor
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {e}")
            raise

    def close_connection(self) -> None:
        """
        Close the connection to the SQLite database.
        """
        if self.connection:
            self.connection.close()

    def export_table_to_csv(self, table_name: str) -> None:
        """
        Export a table from the database to a CSV file.

        Parameters:
        - table_name (str): The name of the table to export.
        """
        try:
            connector = DatabaseConnector(self.database_file)
            sql_conn = connector.connect()
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, sql_conn)

            connector.close_connection()

            df.to_csv(f"{sys.path[1]}\\exported_csv\\{table_name}.csv", index=False)
        except Exception as e:
            logging.error(f"Error exporting {table_name} to CSV: {e}")
            raise
