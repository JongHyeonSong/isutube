from django import forms
from .models import Video, Comment


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields ="__all__"
        exclude = ('author', 'view_count', 'thumbUp',)

        #전체에서 하나만 빼는방법 반드시 마지막에 콤마(',')
        # fields = '__all__'
        # exclude = ('view_count', 'author', )
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            'content' : forms.Textarea(attrs={'rows':3})
        }