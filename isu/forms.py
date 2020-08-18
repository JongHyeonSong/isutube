import os
from django import forms
from .models import Video, Comment


class VideoForm(forms.ModelForm):

    def clean_file(self): #데이터 생성시 이 함수가 실행된다
        file = self.cleaned_data.get('file',None)
        if file:
            extension = os.path.splitext(file.name)[-1].lower()
            if extension not in ('.mp4', '.avi'):
                raise forms.ValidationError('비디오만 업로드해주세요')
            return file

    class Meta:
        model = Video
        fields ="__all__"
        exclude = ('author', 'view_count', 'thumbUp','like',)

        #전체에서 하나만 빼는방법 반드시 마지막에 콤마(',')
        # fields = '__all__'
        # exclude = ('view_count', 'author', )
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]

        widgets = {
            'content' : forms.Textarea(attrs={'rows':3})
        }