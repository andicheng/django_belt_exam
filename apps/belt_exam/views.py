from django.shortcuts import render, redirect, HttpResponse
import random
import string
import datetime
import bcrypt
import re
from .models import User, Trip
from django.contrib import messages

def index(request):
    return render(request, 'belt_exam/index.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confword = request.POST['confword']
        errors = User.objects.validate(first_name, last_name, email, password, confword)
        if len(errors)>0:
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')
        else:
            user = User.objects.register(first_name, last_name, email, password)
            request.session['logged_user'] = user.id
            messages.add_message(request, messages.INFO, "Successfully registered")
            return redirect('/travels')
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
                return redirect('/travels')
            else:
                messages.add_message(request, messages.INFO, "Invalid Login Credentials")
                return redirect('/')
    else:
        return redirect('/')

def travels(request):
    users = User.objects.all()
    user = User.objects.get(id=request.session['logged_user'])
    my_trips = Trip.objects.filter(users=user.id)
    other_trips = Trip.objects.exclude(users=user.id)
    trips = Trip.objects.all()
    context = {
        'my_trips' : my_trips,
        'user' : user,
        'users' : users,
        'trips' : trips,
        'other_trips' : other_trips,
    }
    return render(request, "belt_exam/travels.html", context)

def join(request, id):
    user = User.objects.get(id=request.session['logged_user'])
    trip = Trip.objects.get(id=id)
    trip.users.add(user)
    return redirect('/travels')

def add_plan(request):
    return render(request, 'belt_exam/add.html')

def add(request):
    user = User.objects.get(id=request.session['logged_user'])
    planner_fname=user.first_name
    planner_lname=user.last_name
    destination = request.POST['destination']
    description = request.POST['description']
    travel_start_date = request.POST['travel_start_date']
    travel_end_date = request.POST['travel_end_date']
    trip = Trip.objects.create(planner_fname=planner_fname, planner_lname=planner_lname, destination=destination, description=description, travel_start_date=travel_start_date, travel_end_date=travel_end_date)
    trip.users.add(user)
    return redirect('/travels')

def destination(request, id):
    trip = Trip.objects.get(id=id)
    users = User.objects.all()
    joined = User.objects.filter(trip=trip.id).exclude(first_name=trip.planner_fname)
    context = {
        'trip' : trip,
        'users' : users,
        'joined' : joined,
    }
    return render(request, 'belt_exam/destination.html', context)

def delete(request, id):
    User.objects.get(id=id).delete()
    return redirect('/travels')

def logout(request):
    if "user" in request.session:
        request.session.pop('user')
    return redirect('/')
