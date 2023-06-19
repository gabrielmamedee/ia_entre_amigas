from django.shortcuts import render
from django.http import HttpResponse 
from django.core.paginator import Paginator
from django.http import FileResponse
from .forms import SearchForm
from .models import Palavra
from docx import Document
import pandas as pd
import codecs
import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from django.conf import settings
from django.http import JsonResponse
from .models import Drive_arquivo



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


def search_files(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_word = form.cleaned_data['search_word']
            results = []

            # Diretório onde os arquivos estão localizados
            directory = 'word_cloud/devocionais'

            # Pesquisar arquivos com base na palavra fornecida
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    if filename.endswith('.docx'):
                        file_path = os.path.join(root, filename)
                        doc = Document(file_path)
                        file_content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                        #print(f"Searching file: {filename}")
                        #print(f"Content: {file_content}")
                        count = file_content.lower().count(search_word.lower())  # Contar ocorrências (ignorando maiúsculas e minúsculas)
                        if count > 0:
                            results.append({
                                'name': filename,
                                'path': file_path,
                                'count': count,
                            })

            # Ordenar resultados em ordem decrescente com base no número de ocorrências
            results = sorted(results, key=lambda x: x['count'], reverse=True)

            #print(results)
            return render(request, 'pesquisa.html', {'results': results, 'search_word' : search_word})

    else:
        form = SearchForm()

    return render(request, 'app/search.html', {'form': form})


#API Google Drive
def get_drive_files(request):
    credentials = service_account.Credentials.from_service_account_file(
        os.path.join(settings.BASE_DIR, settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE),
        scopes=settings.GOOGLE_DRIVE_SCOPES
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    page_token = None
    file_data = []
    while True:
        results = drive_service.files().list(fields="nextPageToken, files(name,webViewLink,webContentLink)", pageToken=page_token).execute()
        files = results.get('files', [])

        for file in files:
            file_data.append({
                'name': file['name'],
                'link': file.get('webViewLink', ''),
                'download_link': file.get('webContentLink', '')
            })

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    # Apagar todos os registros existentes
    Drive_arquivo.objects.all().delete()

    for file_info in file_data:
        Drive_arquivo.objects.create(
            nome=file_info['name'],
            link=file_info['link'],
            link_download=file_info['download_link']
        )

    return JsonResponse({'message': 'Dados inseridos com sucesso.'})