from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^add_favorite/(?P<id>\d+)$', views.add_favorite, name='add_favorite'),
    url(r'^add_quote$', views.add_quote),
    url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
    url(r'^users/(?P<id>\d+)$', views.users, name='users'),
    url(r'^logout$', views.logout),
]
