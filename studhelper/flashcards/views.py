from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Flashcard
from .form import FlashcardForm
from topics.models import Topic

def flashcard(request, fk):
    flashcard = get_object_or_404(Flashcard, pk=fk)
    return render(request, "flashcard_page.html", {'flashcard': flashcard})

def create_flashcard(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.topic = topic
            flashcard.save()

    return redirect("topic_detail", pk=topic.pk)

@require_POST
def delete_flashcard(request, pk, fk):
    topic = get_object_or_404(Topic, pk=pk)
    flashcard = get_object_or_404(Flashcard, pk=fk, topic=topic) # скорее всего будет возникать ошибка из-за одинаковых pk
    flashcard.delete()
    return redirect("topic_detail", pk=topic.pk)

def edit_flashcard(request, pk, fk):
    topic = get_object_or_404(Topic, pk=pk)
    flashcard = get_object_or_404(Flashcard, pk=fk, topic=topic)    # скорее всего будет возникать ошибка из-за одинаковых pk
    if request.method == "POST":
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect("topic_detail", pk=topic.pk)
    else:
        form = FlashcardForm(instance=flashcard)
        
    flashcards = Flashcard.objects.filter(topic=topic)
    context = { "form": form, "flashcards": flashcards, "topic": topic }
    return render(request, "topic_page.html", context)
