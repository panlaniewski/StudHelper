from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(
        required=False, 
        max_length=50, 
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск предметов...'
        })
    )