from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = "index"),
    url(r'^login$', views.login, name = "login"),
    url(r'^registration$', views.registration, name = "register"),
    url(r'^friends$', views.friends, name = "friends"),
    url(r'^users/(?P<id>\d+)$', views.users, name = "users"),
    url(r'^add/(?P<id>\d+)$', views.add, name = "add"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = "remove"),
]