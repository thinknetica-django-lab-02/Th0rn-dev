from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, ModelForm
from allauth.account.forms import SignupForm

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


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
