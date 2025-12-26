from django.db import models

class Flashcard(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    answer = models.TextField(blank=True, verbose_name="Ответ")
    topic = models.ForeignKey('topics.Topic', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Тема")

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "Карточки"
        verbose_name_plural = "Карточки"
