from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from .models import Profile, Room


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


ProfileFormset = inlineformset_factory(User, Profile, fields=())


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
