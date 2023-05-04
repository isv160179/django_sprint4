from django.forms import ModelForm, DateTimeInput

from blog.models import Post, Commentary


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('is_published', 'author',)
        widgets = {
            'pub_date': DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'})
        }


class CommentaryForm(ModelForm):
    class Meta:
        model = Commentary
        fields = ('text',)