# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Custom_user

# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     phone_number = forms.CharField(max_length=15, required=True)

#     class Meta:
#         model = Custom_user
#         fields = ('first_name', 'email', 'phone_number', 'password1', 'password2')

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(label='Email', max_length=254)

#     class Meta:
#         model = Custom_user
#         fields = ('email', 'password')


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta:
        model = Custom_user
        fields = ('first_name', 'email', 'phone_number', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    # If you are not leveraging the 'model' directly, you might not need this.
    class Meta:
        fields = ['username', 'password']
