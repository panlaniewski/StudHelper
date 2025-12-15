from django.forms import ModelForm, Textarea
from .models import Topic

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name", "workbook"]
        widgets = {
            "synopsis": Textarea(attrs={
                "rows": 18,
                "placeholder": "Поддерживается Markdown"
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


