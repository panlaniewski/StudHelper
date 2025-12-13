from django.db import models
from django.contrib.auth import get_user_model

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name_plural = "Предметы"
        verbose_name = "Предмет"
        ordering = ["-id"] 

    def __str__(self):
        return self.name