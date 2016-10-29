from __future__ import unicode_literals
import bcrypt
import re
import datetime
import dateutil
from dateutil import parser
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models

class UserManager(models.Manager):

    def validate(self, first_name, last_name, email, password, confword):
        errors=[]
        if len(first_name) ==0:
            errors.append("Please enter a first name")
        elif len(first_name) < 2:
            errors.append("First name must contain at least 2 characters")
        elif not first_name.isalpha():
            errors.append("First name must contain only letters")
        if len(last_name) ==0:
            errors.append("Please enter a last name")
        elif len(last_name) < 2:
            errors.append("last name must contain at least 2 characters")
        elif not last_name.isalpha():
            errors.append("last name must contain only letters")
        if len(email)==0:
            errors.append("Please enter an email address")
        elif not EMAIL_REGEX.match(email):
            errors.append("Please enter a valid email address")
        if len(password) == 0:
            errors.append("Please enter a password")
        elif len(password) < 8:
            errors.append("Password must contain at least 8 characters")
        if confword != password:
            errors.append("Password not confirmed")
        if len(User.objects.filter(email=email))>0:
            errors.append("Email address already registered")
        return errors

    def validate_log(self, email, password):
        errors=[]
        if len(email)==0:
            errors.append("Please enter an email address")
        elif not EMAIL_REGEX.match(email):
            errors.append("Please enter a valid email address")
        if len(password) == 0:
            errors.append("Please enter a password")
        elif len(password) < 8:
            errors.append("Password must contain at least 8 characters")
        return errors

    def register(self, first_name, last_name, email, password):
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, pw_hash=pw_hash)
        return user

    def login(self, post):
        user_list = User.objects.filter(email=post['email'])
        if user_list:
            user = user_list[0]
            print user
            if bcrypt.hashpw(post['password'].encode(), user.pw_hash.encode()) == user.pw_hash:
                return user
        return None

class TripManager(models.Manager):

    def validate(self, travel_start_date, travel_end_date):
        errors=[]
        if travel_start_date > travel_end_date:
            errors.append("Travel-to date must be after Travel-start date")
        travel_start_date = dateutil.parser.parse(travel_start_date)
        if travel_start_date < datetime.datetime.today():
            errors.append("Please enter a travel date in the future")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    members = models.ManyToManyField(User, through='Membership', related_name='members')
    planner = models.ForeignKey(User, related_name='planner',on_delete=models.CASCADE)
    destination = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    travel_start_date = models.DateField(auto_now=False)
    travel_end_date = models.DateField(auto_now=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    objects = TripManager()

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now=True)
