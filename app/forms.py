from django import forms
from django.contrib.auth.models import User
from models import Session

#from models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()
'''

class SessionForm(forms.ModelForm):
    name = forms.CharField(strip = True, max_length=32, min_length=2)
    class Meta:
        model = Session
        fields = ('name',)