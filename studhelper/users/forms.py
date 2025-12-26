from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=False, label="E-mail",  widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'необязательно'}))
    first_name = forms.CharField(required=False, label="Имя",  widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'необязательно'}))
    last_name = forms.CharField(required=False, label="Фамилия",  widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'необязательно'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if email not in [None, '']:     # валидация только если поле не пустое
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError("Такой e-mail уже существует!")
            return email

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(disabled=True, label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': "Имя",
            'last_name': "Фамилия"
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Подтверждение нового пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

