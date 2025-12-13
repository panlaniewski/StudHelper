from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Subject
from django.contrib.auth.decorators import login_required

def subjects_list(request):
    return redirect("home")

@login_required
def subject(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    return render(request, "subject_page.html", {'subject': subject})


