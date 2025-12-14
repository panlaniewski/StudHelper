from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Topic
from .form import TopicForm
from subjects.models import Subject


def topics_list(request, subject_id):
    return HttpResponse(f"Тут все темы предмета {subject_id}!")

def topic(request, pk, slug):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "topic_page.html", {'topic': topic })

def create_topic(request, slug):
    subject = get_object_or_404(Subject, slug=slug)

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subject = subject
            topic.save()

    return redirect("subject_detail", slug=subject.slug)

@require_POST
def delete_topic(request, slug, pk):
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject)
    topic.delete()
    return redirect("subject_detail", slug=subject.slug)

def edit_topic(request, slug, pk):
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject)
    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect("subject_detail", slug=subject.slug)
    else:
        form = TopicForm(instance=topic)
        
    topics = Topic.objects.filter(subject=subject)
    context = { "form": form, "topics": topics, "subject": subject }
    return render(request, "subject_page.html", context)
