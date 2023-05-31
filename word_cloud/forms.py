from django import forms

class SearchForm(forms.Form):
    search_word = forms.CharField(label='Palavra de busca')