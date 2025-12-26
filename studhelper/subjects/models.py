from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import unidecode
from studhelper import settings

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    
    def save(self, *args, **kwargs):
        base_slug = slugify(unidecode.unidecode(self.name))
        if not base_slug:
            base_slug = "subject"
        slug = base_slug
        counter = 1
        while Subject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Предметы"
        verbose_name = "Предметы"
        ordering = ["-id"]

    def get_absolute_url(self):
        return reverse('subject_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name