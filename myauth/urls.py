from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', views.register, name='register'), 
]