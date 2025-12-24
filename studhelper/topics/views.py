from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Topic
from subjects.models import Subject
from flashcards.models import Flashcard
from .form import TopicForm, SynopsisForm
from flashcards.form import FlashcardForm

import markdown


def topics_list(request, subject_id):
    return HttpResponse(f"Тут все темы предмета {subject_id}!")

def topic(request, pk, slug):
    topic = get_object_or_404(Topic, pk=pk)
    flashcards = Flashcard.objects.filter(topic=topic)
    form = FlashcardForm()
    # ------------------------------------------------------------------------------------------------------------------------------

    rendered_workbook = markdown.markdown(
        topic.workbook,
        extensions=["extra", "toc", "codehilite"]
    )
    context = {
        "topic": topic,
        'flashcards': flashcards,
        'form': form,
        "synopsis": rendered_workbook,
    }
    return render(request, "topic_page.html", context)

def create_topic(request, slug):
    subject = get_object_or_404(Subject, slug=slug)

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subject = subject
            topic.save()

    return redirect("subject_detail", slug=subject.slug)

def edit_synopsis(request, slug, pk):
    # topic = get_object_or_404(Topic, pk=pk)

    # if request.method == "POST":
    #     form = SynopsisForm(request.POST, instance=topic)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("topic_detail", pk=topic.pk)
    # else:
    #     form = SynopsisForm(instance=topic)

    # return redirect("topic_detail", pk=topic.pk)

    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject)

    # Получаем существующую заметку пользователя (если есть)
    try:
        synopsis = topic.workbook
    except Topic.DoesNotExist:
        synopsis = None

    if request.method == 'POST':
        form = SynopsisForm(request.POST, instance=topic)
        if form.is_valid():
            note_obj = form.save(commit=False)
            note_obj.save()
            # Redirect после POST (Post/Redirect/Get) — чтобы избежать повторного submit
            return redirect("topic_detail", slug=subject.slug, pk=topic.pk)
    else:
        form = SynopsisForm(instance=topic)

    context = {
        'topic': topic,
        'form': form,
        'synopsis': synopsis,
    }
    return render(request, 'edit_synopsis.html', context)

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