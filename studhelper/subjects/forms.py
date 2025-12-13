from django.forms import ModelForm
from .models import Subject

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"