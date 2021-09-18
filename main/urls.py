from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^day/(?P<pk>\d+-\d+-\d+)$', views.day, name="day"), 
    url(r'^day/(?P<pk>\d+-\d+-\d+)/add$', views.add, name="add"), 
    url(r'^detail/(?P<pk>\d+)$', views.detail, name="detail"),  
    url(r'^remove/(?P<pk>\d+)$', views.remove, name="remove"),  
    url(r'^edit/(?P<pk>\d+)$', views.edit, name="edit"), 
]