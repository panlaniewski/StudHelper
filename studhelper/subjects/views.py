from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
# ---------------------------------------------------------------------------------------------------------------------
from .models import Subject
from django.contrib.auth.decorators import login_required
# ------------------------------------------------------------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------------------------------------------------------------
    keyword = request.GET.get("keyword", "")
    if keyword:
        q = Q(name__icontains=keyword)
        topics = Topic.objects.filter(subject=subject).filter(q)
    else:
        topics = Topic.objects.filter(subject=subject)
    # ------------------------------------------------------------------------------------------------------------------------------       
    paginator = Paginator(topics, 6) 
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    # ------------------------------------------------------------------------------------------------------------------------------
    if request.method == "POST":
        form = TopicForm(request.POST, user=request.user)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subject = subject
            topic.user = request.user
            
            # Автоматически определяем order
            last_topic = Topic.objects.filter(
                user=request.user, 
                subject=subject
            ).order_by('-order').first()
            
            if last_topic:
                topic.order = last_topic.order + 1
            else:
                topic.order = 1
            
            topic.save()
            return redirect("subject_detail", slug=subject.slug)
    else:
        form = TopicForm(user=request.user)
    
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

    