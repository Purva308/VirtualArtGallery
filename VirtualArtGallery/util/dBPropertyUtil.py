import configparser
import os
import urllib.parse

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(file_name):
        try:
            if not os.path.exists(file_name):
                raise FileNotFoundError(f"Properties file '{file_name}' not found.")

            # Initialize config parser
            config = configparser.ConfigParser()
            config.read(file_name)

            # Check if the 'Database' section exists
            if 'Database' not in config:
                raise KeyError("Section 'Database' not found in properties file.")

            hostname = config['Database'].get('db.hostname')
            dbname = config['Database'].get('db.dbname')
            username = config['Database'].get('db.username')
            password = config['Database'].get('db.password')
            port = config['Database'].get('db.port')

            if not all([hostname, dbname, username, password, port]):
                raise ValueError("One or more required database properties are missing")

            # Encode password to handle special characters
            safe_password = urllib.parse.quote(password)

            # Create connection string
            connection_string = f"mysql+mysqlconnector://{username}:{safe_password}@{hostname}:{port}/{dbname}"
            return connection_string

        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f"Error reading properties file: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error in DBPropertyUtil: {str(e)}")
        return None

