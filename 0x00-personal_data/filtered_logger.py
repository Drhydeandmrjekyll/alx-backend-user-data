#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import logging
from filtered_logger import get_db, PII_FIELDS

def main():
    """Retrieve and display rows from the users table with filtered fields."""
    # Connect to the database
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows from the users table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Display each row with filtered fields
    for row in rows:
        filtered_row = {field: '***' if field in PII_FIELDS else value for field, value in zip(cursor.column_names, row)}
        logging.info("name=%s; email=%s; phone=%s; ssn=%s; password=%s; ip=%s; last_login=%s; user_agent=%s",
                     *filtered_row.values())

    # Close the database connection
    cursor.close()
    db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[HOLBERTON] user_data %(levelname)s %(asctime)s: %(message)s")
    main()
