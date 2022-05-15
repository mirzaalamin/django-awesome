from django import forms
from django.contrib.auth.models import User
from Login_app.models import userInfo

class userForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class userInfoForm(forms.ModelForm):
    class Meta():
        model = userInfo
        fields = ('fb_id', 'profile_pic')

class userInfoEditForm(forms.ModelForm):
    class Meta():
        model = userInfo
        fields = ('fb_id',)


class userEditForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('email',)
