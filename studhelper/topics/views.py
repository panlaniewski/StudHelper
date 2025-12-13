from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def topics_list(request, subject_id):
    return HttpResponse(f"Тут все темы предмета {subject_id}!")

@login_required
def topic(request, subject_id, topic_id):
    return HttpResponse(f"Это страница темы {topic_id} предмета {subject_id}!")
