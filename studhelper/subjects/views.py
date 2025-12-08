from django.shortcuts import render
from django.http import HttpResponse

def subjects_list(request):
    return HttpResponse(f"Тут все предметы!")

def subject(request, subject_id):
    return HttpResponse(f"Страница предмета {subject_id}!")


