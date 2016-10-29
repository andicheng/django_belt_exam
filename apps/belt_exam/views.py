from django.shortcuts import render, redirect, HttpResponse
import random
import string
import datetime
import bcrypt
import re
from .models import User, Quote, Favorite
from django.contrib import messages

def index(request):
    return render(request, 'belt_exam/index.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        confword = request.POST['confword']
        date_of_birth = request.POST['date_of_birth']
        print date_of_birth
        errors = User.objects.validate(name, alias, email, date_of_birth, password, confword)
        if len(errors)>0:
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')
        else:
            user = User.objects.register(name, alias, email, date_of_birth, password)
            request.session['logged_user'] = user.id
            messages.add_message(request, messages.INFO, "Successfully registered")
            return redirect('/quotes')
    else:
        return redirect('/')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        errors = User.objects.validate_log(email, password)
        if len(errors) > 0:
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect ('/')
        else:
            user = User.objects.login(request.POST)
            print user
            if user:
                request.session['logged_user'] = user.id
                test = request.session['logged_user']
                print test
                messages.add_message(request, messages.INFO, "Successfully logged-in")
                return redirect('/quotes')
            else:
                messages.add_message(request, messages.INFO, "Invalid Login Credentials")
                return redirect('/')
    else:
        return redirect('/')

def quotes(request):
    # quotes = Quote.objects.all()
    user = User.objects.get(id=request.session['logged_user'])
    my_favorites = Quote.objects.filter(fans = user.id).order_by("-date_added")
    other_quotes = Quote.objects.exclude(fans = user.id).order_by("-date_added")
    # users = User.objects.all()
    context = {
        'user' : user,
        'my_favorites' : my_favorites,
        'other_quotes' : other_quotes,
        'users' : users,
        'quotes' : quotes,
    }
    return render(request, "belt_exam/quotes.html", context)

def add_favorite(request, id):
    quote = Quote.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_user'])
    Favorite.objects.create(user=user, quote=quote)
    return redirect('/quotes')

def add_quote(request):
    if request.method == "POST":
        quote = request.POST['quote']
        author = request.POST['author']
        errors = Quote.objects.validate_quote(quote, author)
        if len(errors) >0:
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect ('/quotes')
        else:
            poster = User.objects.get(id=request.session['logged_user'])
            Quote.objects.create(quote=quote, author=author, poster=poster)
            return redirect('/quotes')
    else:
        return redirect('/')

def remove(request, id):
    quote = Quote.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_user'])
    Favorite.objects.get(quote=quote, user=user).delete()
    return redirect('/quotes')

def users(request, id):
    user = User.objects.get(id=id)
    quotes = Quote.objects.filter(poster=user)
    context = {
        'user': user,
        'quotes': quotes
    }
    return render(request,"belt_exam/users.html", context)

def logout(request):
    if "user" in request.session:
        request.session.pop('user')
    return redirect('/')
