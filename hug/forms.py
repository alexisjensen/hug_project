from django import forms
from django.contrib.auth.models import User
from hug.models import UserProfile, Photo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class PhotoForm(forms.ModelForm):
    tags = forms.CharField(max_length=128, help_text="tags... all lowercase and separate each with a space.")
    class Meta:
        model = Photo
        fields = ('picture', 'comm', 'tags')
