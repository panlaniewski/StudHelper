from django.db import models
# ----------------------------------------------------------------------------------------------------------------------    
class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return self.name
# ----------------------------------------------------------------------------------------------------------------------    
class Flashcard(models.Model):
    quation = models.TextField()
    answer = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.quation
