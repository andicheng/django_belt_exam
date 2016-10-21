from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
    url(r'^add_plan$', views.add_plan),
    url(r'^add$', views.add),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^join/(?P<id>\d+)$', views.join, name='join'),
]
