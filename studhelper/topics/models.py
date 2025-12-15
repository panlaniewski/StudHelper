from django.db import models
# ----------------------------------------------------------------------------------------------------------------------    
class Topic(models.Model):
    name = models.CharField(max_length=200)
    workbook = models.TextField(blank=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return self.name
