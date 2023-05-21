import os
import docx2txt
import re
from collections import Counter

import black_list

pasta = "devocionais"
palavras = []

for raiz, diretorios, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        if arquivo.endswith(".docx"):
            caminho_arquivo = os.path.join(raiz, arquivo)
            texto = docx2txt.process(caminho_arquivo)
            palavras.extend(re.findall(r'\b[A-Za-z]+\b', texto))

contagem = Counter(palavras)
palavras_comuns = contagem.most_common()

palavras_comuns.sort(key=lambda x: x[1], reverse=True)

limite_palavras = 201
contador = 0

caminho_saida = "../templates/static/word_cloud/js/script.js"

with open(caminho_saida, "w") as arquivo_saida:
    arquivo_saida.write("const words = [\n")
    for palavra, frequencia in palavras_comuns:
        if frequencia > 3 and len(palavra) > 2 and palavra not in black_list.blacklist:
            if contador == 0:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 10 }},\n')
                contador += 1
            elif contador == 1:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 8 }},\n')
                contador += 1
            elif contador == 2:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 7 }},\n')
                contador += 1
            elif contador == 3:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 5 }},\n')
                contador += 1
            elif contador > 3 and contador <= 6:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 4 }},\n')
                contador += 1
            elif contador > 6 and contador <= 25:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 3 }},\n')
                contador += 1
            elif contador > 25 and contador <= 65:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 2 }},\n')
                contador += 1
            elif contador > 65 and contador <= 200:
                arquivo_saida.write(f'  {{ key: "{palavra}", value: 1 }},\n')
                contador += 1
            if contador == limite_palavras:
                break

    arquivo_saida.write("];\n\n\n")
    arquivo_saida.write("Chart.defaults.color = '#ffffff';\n")
    arquivo_saida.write("\n")
    arquivo_saida.write("const chart = new Chart(document.getElementById('canvas').getContext('2d'), {\n")
    arquivo_saida.write("  type: 'wordCloud',\n")
    arquivo_saida.write("  data: {\n")
    arquivo_saida.write("    labels: words.map(d => d.key),\n")
    arquivo_saida.write("    datasets: [\n")
    arquivo_saida.write("      {\n")
    arquivo_saida.write("        label: '',\n")
    arquivo_saida.write("        data: words.map(d => 10 + d.value * 10) }] },\n")
    arquivo_saida.write("\n")
    arquivo_saida.write("  options: {\n")
    arquivo_saida.write("    title: {\n")
    arquivo_saida.write("      display: false,\n")
    arquivo_saida.write("      text: 'Chart.js Word Cloud' },\n")
    arquivo_saida.write("\n")
    arquivo_saida.write("    plugins: {\n")
    arquivo_saida.write("      legend: {\n")
    arquivo_saida.write("        display: false } } } });")
