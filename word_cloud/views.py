from django.shortcuts import render
from django.http import HttpResponse 
import json

def view_the_cloud(request):
     my_data = {'p1': 'cidadeviva', 'p2': 'bar'}
     return render(request, 'index.html', {'my_data': my_data})
