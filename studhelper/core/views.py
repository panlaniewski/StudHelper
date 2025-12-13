from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from subjects.models import Subject
from subjects.forms import SubjectForm

def index(request):
    subjects = Subject.objects.all()
    
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            # subject.user = request.user
            subject.save()
            return redirect("home")
    else:
        form = SubjectForm()
        
    context = { "subjects": subjects, "form": form, }
    return render(request, 'index.html', context)

def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена(")
