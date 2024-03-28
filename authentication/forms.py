from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password1', 'password2']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.phone_number = self.cleaned_data['phone_number']
            if commit:
                user.save()

            return user
