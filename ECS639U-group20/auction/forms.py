from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(widget= DateInput,required=True)
    profile_image = forms.ImageField(widget=forms.FileInput)
    city = forms.CharField(widget=forms.TextInput)
    

    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birth', 'profile_image', 'city', 'password1', 'password2']