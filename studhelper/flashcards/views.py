from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Flashcard
from .form import FlashcardForm
from topics.models import Topic
from subjects.models import Subject
import random

@login_required
def flashcard(request, topic_pk, fk):
    topic = get_object_or_404(Topic, pk=topic_pk)
    flashcard = get_object_or_404(Flashcard, pk=fk, topic=topic)
    return render(request, "flashcards/flashcard_detail.html", { 'flashcard': flashcard, 'topic': topic })

@login_required
def create_flashcard(request, slug, pk):
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject, subject__user=request.user)
    
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.topic = topic
            flashcard.save()
            return redirect("topic_detail", slug=subject.slug, pk=topic.pk)
    else:
        form = FlashcardForm()
    
    context = {
        'form': form,
        'topic': topic,
        'subject': subject
    }
    return render(request, "flashcards/flashcard_form.html", context)

@login_required
@require_POST
def delete_flashcard(request, slug, pk, fk):
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject, subject__user=request.user)
    flashcard = get_object_or_404(Flashcard, pk=fk, topic=topic) # скорее всего будет возникать ошибка из-за одинаковых pk
    flashcard.delete()
    return redirect("topic_detail", slug=subject.slug, pk=topic.pk)

@login_required
def edit_flashcard(request, slug, pk, fk):
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject, subject__user=request.user)
    flashcard = get_object_or_404(Flashcard, pk=fk, topic=topic)

    if request.method == "POST":
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect("topic_detail", slug=topic.subject.slug, pk=topic.pk)
    else:
        form = FlashcardForm(instance=flashcard)

    context = {
        "form": form,
        "flashcard": flashcard,
        "topic": topic
    }
    return render(request, "flashcard_edit.html", context)

@login_required
def flashcard_test(request, slug, pk):
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject, subject__user=request.user)
    flashcards = list(Flashcard.objects.filter(topic=topic))
    if not flashcards:
        return redirect('topic_detail', slug=topic.subject.slug, pk=topic.pk)

    random.shuffle(flashcards)
    request.session['trainer_flashcard'] = [f.pk for f in flashcards]
    request.session['trainer_index'] = 0
    request.session['trainer_correct'] = 0  

    return redirect('trainer_flashcard', slug=slug, pk=pk)

def trainer_flashcard(request, slug, pk):
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject, subject__user=request.user)
    flashcards_pks = request.session.get('trainer_flashcard', [])
    index = request.session.get('trainer_index', 0)

    if index >= len(flashcards_pks):
        return redirect('trainer_result', slug=slug, pk=pk)

    flashcard = get_object_or_404(Flashcard, pk=flashcards_pks[index])

    if request.method == "POST":
        request.session['trainer_index'] += 1
        return redirect('trainer_flashcard', slug=slug, pk=pk)

    return render(request, 'trainer_flashcard.html', {
        'topic': topic,
        'flashcard': flashcard,
        'index': index+1,
        'total': len(flashcards_pks)
    })

def trainer_result(request, slug, pk):
    topic = get_object_or_404(Topic, pk=pk, subject__slug=slug)
    total = len(request.session.get('trainer_flashcard', []))
    correct = request.session.get('trainer_correct', 0)

    for key in ['trainer_cards', 'trainer_index', 'trainer_correct']:
        request.session.pop(key, None)

    return render(request, 'flashcards_trainer_result.html', {
        'topic': topic,
        'total': total,
        'correct': correct
    })
