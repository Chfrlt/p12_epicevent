from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import EpiceventsUser

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = EpiceventsUser
        fields = ('username', "role")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Erreur: les mots de passe ne correspondent pas')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EpiceventsUser
        fields = ('username', 'password', 'role', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.role == 1:
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_admin = False
            user.is_superuser = False

        if commit:
            user.save()
        return user
