from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
# ---------------------------------------------------------------------------------------------------------------------
from .models import Subject
from topics.models import Topic
from .forms import SubjectForm
# ---------------------------------------------------------------------------------------------------------------------
def subjects_list(request):
    return redirect("home")
# ---------------------------------------------------------------------------------------------------------------------
def subject(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    topics = Topic.objects.filter(subject=subject)
    context = {'subject': subject, 'topics': topics }
    return render(request, "subject_page.html", context)
# ---------------------------------------------------------------------------------------------------------------------
@require_POST
def subject_delete(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    subject.delete()
    return redirect("home")
# ---------------------------------------------------------------------------------------------------------------------
def subject_edit(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = SubjectForm(instance=subject)
        
    context = {"form": form, "subjects": Subject.objects.all()}
    return render(request, "index.html", context)