from django.urls import path
from . import views 

urlpatterns = [
    path('', views.view_the_cloud, name="view_the_cloud")
]