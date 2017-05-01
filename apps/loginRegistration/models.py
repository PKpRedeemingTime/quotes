from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, postData, request):
        if User.objects.filter(alias = postData['client_alias']).exists():
            hashed = str(User.objects.only('password').get(alias = postData['client_alias']).password)
            if hashed == bcrypt.hashpw(str(postData['client_password']), hashed):
                request.session['id'] = User.objects.only('id').get(alias = postData['client_alias']).id
                request.session['alias'] = User.objects.only('alias').get(alias = postData['client_alias']).alias
                return True
            else:
                messages.warning(request, 'Password does not match alias in our database.')
                return False
        else:
            messages.warning(request, 'alias is not in our database.')
            return False
    def register(self, postData, request):
        if User.objects.filter(alias = postData['alias']).exists():
            messages.error(request, 'alias is already in our database.')
            return False
        else:
            flag = True
            if len(postData['name']) < 2:
                messages.error(request, 'Your first name must be at least two characters.')
                flag = False
            if len(postData['alias']) < 2:
                messages.error(request, 'Your alias must be at least 2 characters.')
                flag = False
            if  not re.match('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
                messages.error(request, 'Your email format is incorrect.')
                flag = False
            if len(postData['password']) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
                flag = False
            if postData['password'] != postData['confirm_password']:
                messages.error(request, 'Your password does not match your password confirmation.')
                flag = False
            if len(postData['birthday']) < 1:
                messages.error(request, 'Please enter your date of birth.')
                flag = False
            if flag == True:
                password = bcrypt.hashpw(str(postData['password']), bcrypt.gensalt())
                User.objects.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = password, birthday = postData['birthday'])
                request.session['id'] = User.objects.only('id').get(email = postData['email']).id
                request.session['alias'] = postData['alias']
                return True
            if flag == False:
                return False

class User(models.Model):
    name = models.CharField(max_length=40)
    alias = models.CharField(max_length=40)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=100)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField('self', through="FriendRelationship", symmetrical=False, related_name="friends+")
    objects = UserManager()

class FriendRelationship(models.Model):
    from_user = models.ForeignKey('User', related_name="from_users")
    to_user = models.ForeignKey('User', related_name="to_users")
    class Meta:
        unique_together = ("from_user", "to_user")