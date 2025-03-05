from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Placeholders
        self.fields["username"].widget.attrs["placeholder"] = "e.g. johndoe"
        self.fields["email"].widget.attrs["placeholder"] = "e.g. johndoe@gmail.com"
        self.fields["password1"].widget.attrs["placeholder"] = "•" * 8
        self.fields["password2"].widget.attrs["placeholder"] = "•" * 8

        # Assign .input class to fields
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "input"

        # Assign Error classes incase of ERRORS
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs["class"] += " form-input-error"

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
