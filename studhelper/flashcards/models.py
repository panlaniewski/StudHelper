from django.db import models

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True)
    topic = models.ForeignKey('topics.Topic', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question
