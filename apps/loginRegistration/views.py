from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.core.urlresolvers import reverse
import bcrypt, datetime
from .models import User, FriendRelationship

def index(request):
    return render(request, 'mainApp/index.html')

def login(request):
    result = User.objects.login(request.POST, request)
    if result == True:
        return redirect(reverse('home:friends'))
    else:
        return redirect(reverse('home:index'))

def registration(request):
    result = User.objects.register(request.POST, request)
    if result == True:
        return redirect(reverse('home:friends'))
    else:
        return redirect(reverse('home:index'))

def friends(request):
    context = {
        "name" : User.objects.get(id = request.session['id']),
        "friends" : User.objects.filter(friends = request.session['id']),
        "count" : User.objects.filter(friends = request.session['id']).count,
        "others" : User.objects.all().exclude(alias = request.session['alias']).exclude(friends = request.session['id']),
    }
    return render(request, 'mainApp/friends.html', context)

def users(request, id):
    context = {
        "client" : User.objects.get(id = id),
    }
    return render(request, 'mainApp/indvusr.html', context)

def add(request, id):
    friend1 = User.objects.get(id = id)
    friend2 = User.objects.get(id = request.session['id'])
    FriendRelationship.objects.create(from_user=friend1, to_user=friend2)
    FriendRelationship.objects.create(from_user=friend2, to_user=friend1)
    return redirect(reverse("home:friends"))

def remove(request, id):
    FriendRelationship.objects.filter(from_user = id).delete()
    FriendRelationship.objects.filter(from_user = request.session['id']).delete()
    return redirect(reverse("home:friends"))