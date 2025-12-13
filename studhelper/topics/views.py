from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Topic

def topics_list(request, subject_id):
    return HttpResponse(f"Тут все темы предмета {subject_id}!")

def topic(request, slug):
    subject = get_object_or_404(Topic, slug=slug)
    return render(request, "subject_page.html", {'subject': subject})
