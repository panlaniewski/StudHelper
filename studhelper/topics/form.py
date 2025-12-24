from django.forms import ModelForm, Textarea

from django import forms
from .models import Topic

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name", "workbook"]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Введите название темы"})}
        
        labels = {
            "name": "Название темы",
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class SynopsisForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["workbook"]
        widgets = {
            "workbook": Textarea(attrs={
                'class': 'form-control autosize',
                "rows": 18,
                "placeholder": "Поддерживается Markdown"
            })
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs["class"] = "form-control"

