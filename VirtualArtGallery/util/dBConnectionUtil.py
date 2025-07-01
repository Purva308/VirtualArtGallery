import mysql.connector
from sqlalchemy import create_engine
from util.dBPropertyUtil import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection(connection_string):
        try:
            if not connection_string:
                raise ValueError("Connection string is None or empty")
            engine = create_engine(connection_string)

            connection=engine.raw_connection()
            return connection
        except Exception as e:
            print(f"Error establishing database connection: {str(e)}")
            return None







