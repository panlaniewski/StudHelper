from django.shortcuts import render
from django.http import HttpResponseNotFound

def index(request):
    return render(request, 'index.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена(")
