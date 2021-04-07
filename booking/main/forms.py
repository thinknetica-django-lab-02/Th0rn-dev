from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from .models import Profile, Room


ProfileFormset = inlineformset_factory(User, Profile, fields=())


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
