from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def add_user(self, postData):
        errors = []
        if not len(postData['name']) > 2:
            errors.append('Name must be be at least 2 characters!')
        if not len(postData['alias']):
            errors.append('Alias must be there!')
        if not len(postData['email']):
            errors.append('Email must be there')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Must have a valid email')
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters long!')
        if not postData['password'] == postData['confirm_password']:
            errors.append('Passwords must match!')
        if not len(postData['birth']):
            errors.append('Birthday must be there')

        user = self.filter(email = postData['email'])

        if user:
            errors.append('Email already exists!')

        modelResponse = {}
        # if failed validations
        if errors:
            modelResponse['status'] = False
            modelResponse['errors'] = errors
        # passed validations, save user
        else:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = hashed_password, birth = postData['birth'])

            modelResponse['status'] = True
            modelResponse['user'] = user

        # send modelResponse to views.py
        return modelResponse

    def check_user(self, postData):
        errors = []
        user = self.filter(email = postData['email'])
        # check to see is in db
        modelResponse = {}
        if user[0]:
            # check for passwords
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors.append('Invalid email/password combination!')
            # success login
            else:
                modelResponse['status'] = True
                modelResponse['user_id'] = user[0].id
        else:
            errors.append('Invalid email')

        if errors:
            modelResponse['status'] = False
            modelResponse['errors'] = errors

        return modelResponse

    def pokes(self, postData):
        self.create(user = User.objects.get(id = postData['user_id']), poke = postData['poke'])

class User(models.Model):
    name = models.CharField(max_length = 45)
    alias = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Poke(models.Model):
    user = models.ForeignKey(User, related_name="user")
    poke = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
