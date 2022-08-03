from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):

    class Meta:
        fields = '__all__'
        model = Comment

