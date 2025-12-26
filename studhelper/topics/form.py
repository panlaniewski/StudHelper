from django.forms import ModelForm
from django import forms
from subjects.models import Subject
from .models import Topic
from django_ckeditor_5.widgets import CKEditor5Widget

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Введите название темы"}),
            }
        
        labels = {
            "name": "Название темы",
        }
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)     # сохраняем текущего пользователя для валидации
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        topic_name = self.cleaned_data['name']
        if topic_name not in [None, '']:     # валидация только если поле не пустое
            if Topic.objects.filter(user=self.user, name=topic_name).exists():
                raise forms.ValidationError("Тема с таким именем уже существует!")
            return topic_name



class SynopsisForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name", "workbook"]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название темы'
            }),
            # 'order': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'is_archived': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'workbook': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, 
                config_name='default'
                ),
        }
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and 'subject' in self.fields:
            self.fields['subject'].queryset = Subject.objects.filter(user=self.user)
    


