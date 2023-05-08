from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class ProfileEdit(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
