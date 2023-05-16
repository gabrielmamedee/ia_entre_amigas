from django.shortcuts import render
from django.http import HttpResponse 
import json

def view_the_cloud(request):
     
     if request.method == "GET":
          return render(request, 'index.html')
     
     elif request.method == "POST":
          palavras = request.POST.get('valor')
          print(palavras)
          return render(request, 'pesquisa.html', {'palavras':palavras})
