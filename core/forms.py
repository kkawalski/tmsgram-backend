from django.forms import ModelForm, Form
from django.forms.fields import CharField
from django.contrib.auth.forms import UserCreationForm, UsernameField

from core.models import User


class SearchForm(Form):
    text = CharField()

    class Meta:
        fields = [
            "text"
        ]


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar"
        ]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}
