from __future__ import unicode_literals
import bcrypt
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models

class UserManager(models.Manager):

    def validate(self, name, alias, email, date_of_birth, password, confword):
        errors=[]
        if len(name) ==0:
            errors.append("Please enter a name")
        elif len(name) < 2:
            errors.append("Name must contain at least 5 characters")
        elif not all(x.isalpha() or x.isspace() for x in name):
            errors.append("Name must contain only letters")
        if len(alias) ==0:
            errors.append("Please enter an alias")
        elif len(alias) < 2:
            errors.append("Alias must contain at least 2 characters")
        if len(email)==0:
            errors.append("Please enter an email address")
        elif not EMAIL_REGEX.match(email):
            errors.append("Please enter a valid email address")
        if len(date_of_birth)==0:
            errors.append("Please enter a bith date")
        else:
            try:
                bday = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
                if bday.date() > datetime.date.today():
                    errors.append("The birth date cannot be in the future")
            except:
                errors.append("Please enter a valid date for the birth date field")
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

    def register(self, name, alias, email, date_of_birth, password):
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name=name, alias=alias, email=email, date_of_birth=date_of_birth, pw_hash=pw_hash)
        return user

    def login(self, post):
        user_list = User.objects.filter(email=post['email'])
        if user_list:
            user = user_list[0]
            print user
            if bcrypt.hashpw(post['password'].encode(), user.pw_hash.encode()) == user.pw_hash:
                return user
        return None

class QuoteManager(models.Manager):
    def validate_quote(self, quote, author):
        errors=[]
        if len(quote)<11:
            errors.append("Please enter a quote longer than 10 characters in length")
        if len(author)<4:
            errors.append("Please enter an author name longer than 3 characters or Unknown")
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    date_of_birth = models.DateField(auto_now=False)
    pw_hash = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    fans = models.ManyToManyField(User, through='Favorite', related_name='fans')
    quote = models.CharField(max_length=45)
    poster = models.ForeignKey(User, related_name="poster", on_delete=models.CASCADE)
    author = models.CharField(max_length=45)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
