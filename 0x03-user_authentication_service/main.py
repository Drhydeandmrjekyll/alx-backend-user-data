#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

my_db = DB()

user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

# Find user by email
find_user = my_db.find_user_by(email="test@test.com")

# If find_user is a list of users
if isinstance(find_user, list):
    for user in find_user:
        print(user.id)
else:
    # If find_user is a single user
    print(find_user.id)

