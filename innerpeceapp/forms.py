from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,Tour,TourPhoto


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Enter password'}),
        required=False
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Confirm password'}),
        required=False
    )

    edit_access = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.Select(attrs={'class': 'form-control p-2 mb-5'}),
        required=True,
        initial='no'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control p-2  mb-5', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control p-2  mb-5', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Enter password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']




class TourForm(forms.ModelForm):
    checkboxes = forms.MultipleChoiceField(
        choices=[
            ('option1', 'Option 1'),
            ('option2', 'Option 2'),
            ('option3', 'Option 3'),
            ('option4', 'Option 4'),
            ('option5', 'Option 5'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Tour
        fields = [
            'title', 'category', 'keyword', 'description', 'day1', 
            'day2', 'day3', 'location', 'checkboxes', 'price', 'date', 'time'
        ]