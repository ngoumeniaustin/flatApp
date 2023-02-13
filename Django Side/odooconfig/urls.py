from django.urls import path
from . import views
app_name = 'odooconfig'

urlpatterns = [
            path('', views.index, name='index'),
            path('connection', views.connection, name='connection'),
            ]