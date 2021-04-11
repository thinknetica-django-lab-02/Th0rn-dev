from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, ModelForm
from .models import Profile, Room


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', "last_name", "email"]


class ProfileForm(ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('birthday', 'user')


ProfileFormset = inlineformset_factory(User, Profile, fields=('birthday',), can_delete=False, extra=0, min_num=1)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
