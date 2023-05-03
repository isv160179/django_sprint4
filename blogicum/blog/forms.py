from django.forms import ModelForm, DateTimeInput

from blog.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('is_published', 'author',)
        widgets = {
            'pub_date': DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'})
        }
