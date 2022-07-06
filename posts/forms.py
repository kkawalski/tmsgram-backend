from django.forms import ModelForm, HiddenInput

from posts.models import Post


class PostCreateForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["user"].initial = self.user
        self.fields["user"].widget = HiddenInput()

    class Meta:
        model = Post
        fields = [
            "description",
            "user",
            "image",
        ]
