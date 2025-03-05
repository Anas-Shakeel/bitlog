from django import forms
from .models import BlogPost, Comment


class BlogPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cover_image"].widget = forms.widgets.FileInput(
            attrs={
                "id": "file-upload",
                "class": "hidden",
                "onchange": "sub(this)",
                "required": False,
            }
        )

        # Title
        self.fields["title"].widget.attrs["class"] = "form-input"
        self.fields["title"].widget.attrs[
            "placeholder"
        ] = "Write an attention-grabbing title..."

        # Caption
        self.fields["caption"].widget.attrs["class"] = "form-input"
        self.fields["caption"].widget.attrs[
            "placeholder"
        ] = "Briefly describe what your post is about..."

        # Content
        self.fields["content"].widget.attrs["class"] = "form-input"
        self.fields["content"].widget.attrs["rows"] = "12"
        self.fields["content"].widget.attrs[
            "placeholder"
        ] = "Start writing your post in Markdown..."

        # Category
        self.fields["category"].widget.attrs["class"] = "form-input form-select"

        # Append Error classes incase of ERRORS
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs["class"] += " form-input-error"

    class Meta:
        model = BlogPost
        fields = [
            "cover_image",
            "title",
            "caption",
            "content",
            "category",
            # "tags",
        ]


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs["rows"] = "4"
        self.fields["content"].widget.attrs["class"] = "form-input"
        self.fields["content"].widget.attrs[
            "placeholder"
        ] = "What are your thoughts on this?"

    class Meta:
        model = Comment
        fields = ["content"]
