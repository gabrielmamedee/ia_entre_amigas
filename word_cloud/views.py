from django.shortcuts import render
from django.http import HttpResponse 
import json
import os
import pandas as pd
from .models import Palavra
from django.core.paginator import Paginator


def view_the_cloud(request):
     
     if request.method == "GET":
          # Recupere os dados da tabela
          palavras = Palavra.objects.all()

          palavra_paginator = Paginator(palavras, 50)
          page_num = request.GET.get('page')
          page = palavra_paginator.get_page(page_num)

          # Renderize o template com os dados
          return render(request, 'index.html', {'page': page})
          
     
     elif request.method == "POST":
          valor = request.POST.get('valor')

          return render(request, 'pesquisa.html', {'valor':valor})
     

def importar_dados(request):
    # Caminho do arquivo Excel
    arquivo_excel = 'word_cloud/import_data.xlsx'

    # Apagar todos os registros existentes
    Palavra.objects.all().delete()

    # Ler o arquivo Excel usando o pandas
    df = pd.read_excel(arquivo_excel)

    # Percorrer as linhas do DataFrame
    for _, row in df.iterrows():
        # Criar uma instância do modelo e definir os valores dos campos
        objeto = Palavra()
        objeto.key = row['key']
        objeto.frequencia = row['frequencia']
        # Definir outros campos conforme necessário

        # Salvar o objeto no banco de dados
        objeto.save()

    # Retornar uma resposta adequada, como uma mensagem de sucesso
    return HttpResponse('Dados importados com sucesso!')
