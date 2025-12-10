from django.shortcuts import render
from django.http import HttpResponseNotFound
from subjects.models import Subject

def index(request):
    subjects = Subject.objects.all()
    return render(request, 'index.html', { "subjects": subjects })

def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена(")
