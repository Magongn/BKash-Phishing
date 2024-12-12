import logging
import sys
import configparser
import sentry_sdk
from datetime import datetime
from time import sleep
from sentry_sdk.integrations.logging import LoggingIntegration
import os
import asyncio

# Initialize Sentry for error monitoring
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'), # Ensure you set your Sentry DSN in the environment variables
    integrations=[sentry_logging]
)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("error_log.log"),
                        logging.StreamHandler(sys.stdout)
                    ])

# Load configurations
config = configparser.ConfigParser()
config.read('config.ini')

class CustomError(Exception):
    """Custom exception class"""
    pass

async def async_sleep(seconds):
    """Asynchronous sleep function"""
    await asyncio.sleep(seconds)

async def divide_numbers(a, b):
    """Function to divide two numbers with error handling and retries"""
    max_retries = config.getint('RETRY', 'max_retries', fallback=3)
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempt {attempt + 1}: Dividing {a} by {b}")
            return a / b
        except ZeroDivisionError as e:
            logging.error(f"Attempt {attempt + 1}: Attempted to divide by zero. Error: {e}")
            if attempt < max_retries - 1:
                await async_sleep(1)  # Wait before retrying
            else:
                print("Error: Cannot divide by zero.")
        except TypeError as e:
            logging.error(f"Attempt {attempt + 1}: Invalid input types. Error: {e}")
            print("Error: Invalid input types. Please enter numbers.")
            break
        except Exception as e:
            logging.critical(f"Attempt {attempt + 1}: An unexpected error occurred. Error: {e}")
            print("An unexpected error occurred.")
            break

async def read_file(file_path):
    """Function to read a file with error handling and retries"""
    max_retries = config.getint('RETRY', 'max_retries', fallback=3)
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempt {attempt + 1}: Reading file {file_path}")
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError as e:
            logging.error(f"Attempt {attempt + 1}: File not found. Error: {e}")
            if attempt < max_retries - 1:
                await async_sleep(1)  # Wait before retrying
            else:
                print("Error: File not found.")
        except IOError as e:
            logging.error(f"Attempt {attempt + 1}: IO error occurred. Error: {e}")
            if attempt < max_retries - 1:
                await async_sleep(1)  # Wait before retrying
            else:
                print("Error: An IO error occurred.")
        except Exception as e:
            logging.critical(f"Attempt {attempt + 1}: An unexpected error occurred. Error: {e}")
            print("An unexpected error occurred.")
            break

async def raise_custom_error(condition):
    """Function to raise a custom error"""
    try:
        if condition:
            raise CustomError("This is a custom error.")
    except CustomError as e:
        logging.error(f"Custom error occurred. Error: {e}")
        print(e)

async def main():
    # Example usage of the divide_numbers function
    print(await divide_numbers(10, 2))  # Should print 5.0
    print(await divide_numbers(10, 0))  # Should print an error message

    # Example usage of the read_file function
    print(await read_file('example.txt'))  # Should print the file content or an error message
    print(await read_file('nonexistent.txt'))  # Should print an error message

    # Example usage of the raise_custom_error function
    await raise_custom_error(True)  # Should raise and print the custom error message

if __name__ == '__main__':
    asyncio.run(main())
