from django.shortcuts import render
from django.http import HttpResponse 
import json
import os
from word_counter import palavras_comuns

def view_the_cloud(request):
     
     if request.method == "GET":
          return render(request, 'index.html')
          
     
     elif request.method == "POST":
          valor = request.POST.get('valor')

          
          return render(request, 'pesquisa.html', {'valor':palavras_comuns[200]})