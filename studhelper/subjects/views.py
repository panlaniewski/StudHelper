from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
# ---------------------------------------------------------------------------------------------------------------------
from .models import Subject
from django.contrib.auth.decorators import login_required

from topics.models import Topic
from .forms import SubjectForm
from topics.form import TopicForm
# ---------------------------------------------------------------------------------------------------------------------
@login_required
def subjects_list(request):
    return redirect("home")
# ---------------------------------------------------------------------------------------------------------------------
@login_required
def subject(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    topics = Topic.objects.filter(subject=subject)
    form = TopicForm()
    
    keyword = request.GET.get("keyword", "")
    if keyword:
        q = Q(name__icontains=keyword)
        topics = Topic.objects.filter(subject=subject).filter(q)
    else:
        topics = Topic.objects.filter(subject=subject)
           
    paginator = Paginator(topics, 6) 
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    
    context = {
        'subject': subject,
        'topics': page.object_list,
        'form': form,
        'page': page,
        'keyword': keyword,
    }
    return render(request, "subject_page.html", context)
# ---------------------------------------------------------------------------------------------------------------------
@require_POST
def subject_delete(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    subject.delete()
    return redirect("home")
# ---------------------------------------------------------------------------------------------------------------------
@login_required
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
# ---------------------------------------------------------------------------------------------------------------------

    