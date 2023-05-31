from django.urls import path
from . import views 

urlpatterns = [
    path('', views.view_the_cloud, name="view_the_cloud"),
    path('importar_dados/', views.importar_dados, name='importar_dados'),
    path('busca/', views.search_files, name='search_files')
]