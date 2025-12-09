from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, null=True) # Связь с моделью Subject(null=True для тестирования, потом обязательно поменять!)


    def __str__(self):
        return self.name
    

class Flashcard(models.Model):
    quation = models.TextField()
    answer = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.quation
