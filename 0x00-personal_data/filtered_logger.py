#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import logging
import os
import mysql.connector


def get_db():
    """Return a connector to MySQL database."""
    # Get database credentials from environment variables
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to MySQL database
    db = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=dbname
    )

    return db


def main():
    """Retrieve and display rows from users table with filtered fields."""
    # Defines PII_FIELDS containing 5 fields of personal identifiable info
    PII_FIELDS = ("name", "email", "phone", "ssn", "credit_card")

    # Connect to database
    db = get_db()
    cursor = db.cursor()

    # Retrieves all rows from users table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Display each row with filtered fields
    for row in rows:
        # Create dictionary comprehension to filter sensitive fields
        filtered_row = {
            field: '***' if field in PII_FIELDS else value
            for field, value in zip(cursor.column_names, row)
        }

        # Use string formatting to log the filtered row
        log_message = "; ".join(
                f"{field}={value}" for field, value in filtered_row.items()
        )

        # Log the filtered row
        logging.info(log_message)

    # Closes database connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[HOLBERTON] user_data %(levelname)s %(asctime)s: %(message)s"
    )
    main()
