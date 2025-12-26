from django import forms
from django.forms import ModelForm
from .models import Subject

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)    # сохраняем текущего пользователя для валидации
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        subject_name = self.cleaned_data['name']
        if subject_name not in [None, '']:     # валидация только если поле не пустое
            if Subject.objects.filter(user=self.user, name=subject_name).exists():
                raise forms.ValidationError("Предмет с таким именем уже существует!")
            return subject_name
            