from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Topic, TopicVersion
from subjects.models import Subject
from flashcards.models import Flashcard
from .form import TopicForm, SynopsisForm
from flashcards.form import FlashcardForm
from django.contrib import messages


def topics_list(request, subject_id):
    return HttpResponse(f"Тут все темы предмета {subject_id}!")

def topic(request, pk, slug):
    topic = get_object_or_404(Topic, pk=pk)
    flashcards = Flashcard.objects.filter(topic=topic)
    form = FlashcardForm()  # форма для создания карточки
    # ------------------------------------------------------------------------------------------------------------------------------

    # Получаем изображения из контента
    images = topic.get_images()

   # Получаем следующую тему (по порядку или по дате создания)
    next_topic = Topic.objects.filter(
        subject=topic.subject,
        created_at__gt=topic.created_at
    ).order_by('created_at').first()
    
    # Если нет по дате, ищем по порядку
    if not next_topic and hasattr(Topic, 'order'):
        next_topic = Topic.objects.filter(
            subject=topic.subject,
            order__gt=topic.order
        ).order_by('order').first()
    
    prev_topic = Topic.objects.filter(
        user=request.user,
        subject=topic.subject,
        order__lt=topic.order,
        is_archived=False
    ).order_by('-order').first()

    context = {
        "topic": topic,
        'images': images,
        'next_topic': next_topic,
        'prev_topic': prev_topic,
        'flashcards': flashcards,
        'form': form,
        # "synopsis": rendered_workbook,
    }

    return render(request, "topic_page.html", context)

# def create_topic(request, slug):
#     subject = get_object_or_404(Subject, slug=slug)

#     if request.method == "POST":
#         form = TopicForm(request.POST, user=request.user)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.subject = subject
#             topic.user = request.user
            
#             # Автоматически определяем order
#             last_topic = Topic.objects.filter(
#                 user=request.user, 
#                 subject=subject
#             ).order_by('-order').first()
            
#             if last_topic:
#                 topic.order = last_topic.order + 1
#             else:
#                 topic.order = 1
            
#             topic.save()
#             return redirect("subject_detail", slug=subject.slug)
#     else:
#         form = TopicForm(user=request.user)
    
    

    
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
    return render(request, "subject_page.html", context)\

def topic_restore_version(request, slug, pk, version_id):
    """Восстановление версии темы"""
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject)
    version = get_object_or_404(TopicVersion, pk=version_id, topic=topic)
    
    topic.workbook = version.content
    topic.save()
    
    messages.success(request, f'Тема восстановлена до версии от {version.created_at.strftime("%d.%m.%Y %H:%M")}')
    return redirect("topic_detail", slug=subject.slug, pk=topic.pk)

def topic_archive(request, slug, pk):
    """Архивирование/разархивирование темы"""
    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject)
    topic.is_archived = not topic.is_archived
    topic.save()
    
    action = "архивирована" if topic.is_archived else "восстановлена из архива"
    messages.success(request, f'Тема "{topic.name}" {action}')
    return redirect("subject_detail", slug=subject.slug)

def edit_synopsis(request, slug, pk):

    subject = get_object_or_404(Subject, slug=slug)
    topic = get_object_or_404(Topic, pk=pk, subject=subject)

    if request.method == 'POST':
        form = SynopsisForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save()
            
            # Проверяем, какую кнопку нажали
            if 'save_and_continue' in request.POST:
                messages.success(request, 'Конспект сохранен. Продолжайте редактирование.')
                return redirect('edit_synopsis', slug=subject.slug, pk=topic.pk)
            elif 'save_and_return' in request.POST:
                messages.success(request, 'Конспект сохранен.')
                return redirect('topic_detail', slug=subject.slug, pk=topic.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = SynopsisForm(instance=topic)
    

    context = {
        'topic': topic,
        'form': form,
    }

    return render(request, 'edit_synopsis.html', context)
    
    