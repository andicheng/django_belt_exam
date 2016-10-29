from django.shortcuts import render, redirect, HttpResponse
import random
import string
import datetime
import bcrypt
import re
from .models import User, Trip, Membership
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
    my_trips = Trip.objects.filter(members=user.id)
    other_trips = Trip.objects.exclude(members=user.id)
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
    Membership.objects.create(user=user, trip=trip)
    return redirect('/travels')

def add_plan(request):
    return render(request, 'belt_exam/add.html')

def add(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session['logged_user'])
        destination = request.POST['destination']
        description = request.POST['description']
        travel_start_date = request.POST['travel_start_date']
        travel_end_date = request.POST['travel_end_date']
        errors = Trip.objects.validate(travel_start_date, travel_end_date)
        if len(errors) >0:
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect ('/add_plan')
        else:
            trip = Trip.objects.create(planner=user, destination=destination, description=description, travel_start_date=travel_start_date, travel_end_date=travel_end_date)
            Membership.objects.create(user=user, trip = trip)
            return redirect('/travels')
    else:
        return redirect('/travels')

def destination(request, id):
    trip = Trip.objects.get(id=id)
    users = User.objects.filter(membership__trip=trip).exclude(id=trip.planner.id)
    context = {
        'trip' : trip,
        'users' : users,
    }
    return render(request, 'belt_exam/destination.html', context)

def delete(request, id):
    User.objects.get(id=id).delete()
    return redirect('/travels')

def logout(request):
    if "user" in request.session:
        request.session.pop('user')
    return redirect('/')
