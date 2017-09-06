from __future__ import unicode_literals

from django.db import models
import bcrypt, re
from datetime import datetime

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+.[^@\s]+$")


class UserManager(models.Manager):
    def validate_and_register(self, postData):
        errors = {}
        
        # Name Validation
        if not len(postData['name']):
            errors['name'] = "Name field can not be empty."
        elif len(postData['name']) < 3:
            errors['name'] = "Name too short."
        
        # Alias Validation
        if not len(postData['alias']):
            errors['alias'] = "Alias field can not be empty."
        elif len(postData['alias']) < 3:
            errors['alias'] = "Alias too short."
        elif self.filter(alias = postData['alias']):
            errors['alias'] = "Error! Alias already in use."
        
        # Email Validation
        if not len(postData['email']):
            errors['email'] = "Email field can not be empty."
        elif not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Invalid email! Please input the right format of an email like: user@mail.com"
        elif self.filter(email = postData['email']):
            errors['email'] = "Error! Email already in use."

        # Password Validation
        if not len(postData['password']):
            errors['password'] = "Password field can not be empty."
        elif len(postData['password']) < 8:
            errors['password'] = "Password too short. Input at least 8 characters"
        elif postData['password'] != postData['confirm_pass']:
            errors['confirm_pass'] = "Password not confirmed. Please pay more attention"
        
        # Birthday validation
        if not postData['birthday']:
            errors['birthday'] = "Birthday field can not be empty."
        else:
            now = datetime.today().date()
            birthday = datetime.strptime(postData['birthday'], "%Y-%m-%d").date()
            # print now - birthday, "$#$##$#$#$#$#$#$#()()()(_(_)(_+(+_()+_(+(+_"
            if birthday >= now:
                errors['birthday'] = "Birthday can not be earlier than the current day."

        # Return of the validation results for register method
        if len(errors):
            return (False, errors)
        else:
            password = postData['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = hashed, birthday = birthday)
            return (True, postData['name'])

    def validate_and_login(self, postData):
        errors_login = {}
        # Email Validation when Login
        if not len(postData['email']):
            errors_login['login_email_error'] = "Please provide an email."
        else:
            if not self.filter(email = postData['email']):
                errors_login['login_error'] = "Email or password wrong."
        
        if not len(errors_login):
            user = self.filter(email = postData['email'])
        # # Password Validation when Login
            if not len(postData['password']):
                errors_login['login_password_error'] = "Please provide password."
            else:
                password = postData['password'].encode()
                hashed = self.filter(email = postData['email'])[0].password.encode()
                if not bcrypt.checkpw(password, hashed):
                    errors_login['login_error'] = "Email or password wrong."

        
        # Return of the validation results for login method
        if len(errors_login):
            return (False, errors_login)
        else:
            return (True, self.filter(email = postData['email']))






class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
# Create your models here.
