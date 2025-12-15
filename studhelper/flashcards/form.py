from django.forms import ModelForm
from django import forms
from .models import Flashcard

class FlashcardForm(ModelForm):
    class Meta:
        model = Flashcard
        fields = ('question', 'answer')
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите вопрос...'}),
            'answer': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите ответ (необязательно)...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"