from __future__ import unicode_literals

from django.db import models
import bcrypt
from time import strftime
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def registration_validaiton(self, postData):

        # List will catch user validation errors and display them at the end.
        errors = []
        print(postData)

        # Name requires at least one character.
        if len(postData["Name"]) < 1:
            errors.append("Name cannot be empty.")
        elif len(postData["Name"]) < 3:
            errors.append("Name must be 3 or more characters")

        # Email requires at least one character.
        if len(postData["Email"]) < 1:
            errors.append("Email cannot be empty.")
        elif len(postData["Email"]) < 5:
            errors.append("Email must be 5 ore more characters.")
        elif not EMAIL_REGEX.match(postData["Email"]):
            errors.append("Invalid Email Address!")

        # Password must be 8 or more characters
        if len(postData["Password"]) < 8:
            errors.append("Password must be 8 or more characters.")

        # Password needs to be confirmed.
        elif postData["PasswordConfirm"] != postData["Password"]:
            errors.append("Passwords do not match.")

        # Emails cannot be dupes.
        all_users = self.all()
        for items in all_users:
            if postData["Email"] in items.email:
                errors.append("Email is taken. Please select a different Email.")

        if postData["birthday"][:4] >= strftime("%Y") and postData["birthday"][5:7] >= strftime("%m") and \
                        postData["birthday"][8:10] >= strftime("%d"):
            errors.append("Your birthday cannot be from the future!")

        # Dictionary to return to the user if validations passed and creating a new user with encrypted password.
        response_to_views = {}

        if len(errors):
            response_to_views["status"] = False
            response_to_views["errors"] = errors
        else:
            response_to_views["status"] = True
            encode_password = postData["Password"].encode()
            hashed_password = bcrypt.hashpw(encode_password, bcrypt.gensalt())
            new_user = self.create(name=postData["Name"], email=postData["Email"], password=hashed_password)
            response_to_views["new_user"] = new_user

        return response_to_views

    def login_validation(self, postData):

        errors = []
        # Email must exist and Email/Password cannot be empty.

        if len(postData["Email"]) < 1:
            errors.append("Email cannot be empty.")
        elif len(postData["Email"]) < 5:
            errors.append("Email must be 5 ore more characters.")
        elif not EMAIL_REGEX.match(postData["Email"]):
            errors.append("Invalid Email Address!")

        if len(postData["PasswordLogin"]) < 1:
            errors.append("Password cannot be empty.")

        elif len(postData["PasswordLogin"]) < 8:
            errors.append("Password must be 8 or more characters long.")
        else:

            # Validate Email matches Password in Database.
            user = self.filter(email=postData["Email"])

            if len(user):
                user = self.get(email=postData["Email"])
                encode_password = postData["PasswordLogin"].encode()
                if bcrypt.hashpw(encode_password, salt=user.password.encode()) != user.password:
                    errors.append("Password and Email do not match.")
            else:
                errors.append("Email not found.")

        # Dictionary will be returned.
        response_to_views = {}

        if len(errors):
            response_to_views["status"] = False
            response_to_views["errors"] = errors
        else:
            response_to_views["status"] = True
            response_to_views["user"] = user.name
            response_to_views["full_user"] = user.id

        return response_to_views


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
