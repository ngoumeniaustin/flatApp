from django.urls import path
from . import views
app_name = 'odoorealtor'

urlpatterns = [
            path('', views.realtor, name='realtor'),
            path('offer', views.offer, name='offer'),
             
            ]