from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags
from studhelper import settings
# ----------------------------------------------------------------------------------------------------------------------    
class Topic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topics', verbose_name="Пользователь", default=1)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Предмет")

    name = models.CharField(max_length=200, verbose_name="Название")
    workbook = CKEditor5Field(
        verbose_name="Конспект",
        config_name='default',
        blank=True,
        null=True)
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_archived = models.BooleanField(default=False, verbose_name="В архиве")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
   
    def __str__(self):
        return f"{self.subject.name}: {self.name}"

    class Meta:
        verbose_name = "Темы"
        verbose_name_plural = "Темы"
        ordering = ['order', 'name']

    def get_absolute_url(self):
        return reverse(
            'topic_detail',
            kwargs={
                'slug': self.subject.slug,
                'pk': self.pk
            }
        )

    def get_preview_text(self, length=150):
        """Текст для предпросмотра без HTML тегов"""
        if not self.content:
            return ""
        text = strip_tags(self.content)
        if len(text) > length:
            return text[:length] + '...'
        return text
    
    def get_images(self):
        """Извлечение всех изображений из контента"""
        import re
        if not self.workbook:
            return []
        
        # Ищем все img теги в контенте
        img_tags = re.findall(r'<img[^>]+src="([^">]+)"', self.workbook)
        return img_tags
    
    def word_count(self):
        """Подсчет слов в конспекте"""
        if not self.workbook:
            return 0
        text = strip_tags(self.workbook)
        words = text.split()
        return len(words)
    

class TopicVersion(models.Model):
    """История изменений темы"""
    topic = models.ForeignKey(
        Topic, 
        on_delete=models.CASCADE, 
        related_name='versions', 
        verbose_name="Тема"
    )
    content = models.TextField(verbose_name="Содержимое")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    
    class Meta:
        verbose_name = "Версия темы"
        verbose_name_plural = "Версии тем"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Версия от {self.created_at.strftime('%d.%m.%Y %H:%M')}"

# Сигналы для сохранения версий
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Topic)
def create_topic_version(sender, instance, **kwargs):
    """Создаем версию при каждом сохранении темы"""
    if instance.workbook:
        if instance.workbook.strip():
            TopicVersion.objects.create(
                topic=instance,
                content=instance.workbook
            )