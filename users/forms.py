from django.forms import ModelForm, widgets
from .models import Profile


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["profile_picture"].widget = widgets.FileInput(
            attrs={
                "id": "file-upload",
                "class": "hidden",
                "onchange": "sub(this)",
                "required": False,
            }
        )

        self.fields["fullname"].widget.attrs["class"] = "form-input"
        self.fields["bio"].widget.attrs["class"] = "form-input"
        self.fields["bio"].widget.attrs["rows"] = "4"

        # Append Error classes incase of ERRORS
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs["class"] += " form-input-error"

    class Meta:
        model = Profile
        fields = ["profile_picture", "fullname", "bio"]
