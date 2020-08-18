from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Video(models.Model):
  
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField()
    file = models.FileField()
    view_count = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    #모델 수정/업데이트후에 여기로 오게된다
    def get_absolute_url(self):
        return reverse('isu:video_detail', args=[self.pk])

    class Meta: 
        ordering=['-id']
    
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-id']
    