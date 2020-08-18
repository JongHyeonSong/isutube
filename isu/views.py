import os
from django.shortcuts import render, get_object_or_404, resolve_url, redirect
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView,ListView
from .models import Video, Comment
from .forms import VideoForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import F
from django.contrib.auth.decorators import login_required

class VideoListView(ListView):
    model = Video
    paginate_by= 3


    def get_queryset(self):
        videoList = super().get_queryset()
        videoListFilter = self.request.GET.get('q','').strip() #form에서 name=q인걸 찾고 아니면 공백
        if videoListFilter:
            videoList = videoList.filter(title__icontains=videoListFilter)
        
        return videoList


class VideoCreateView(LoginRequiredMixin, CreateView):
    form_class = VideoForm
    model = Video
    template_name = 'form.html'

    def form_valid(self, form):
        video = form.save(commit=False) #여기서 false를 해줘야 2중으로 커밋되지않는다
        video.author = self.request.user
        return super().form_valid(form)

class VideoDetailView(DetailView):
    model = Video

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        Video.objects.filter(id=pk).update(view_count = F('view_count')+1)
        return super().get_object(queryset=queryset)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context

class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'form.html'

    def test_func(self):
        return self.request.user == self.get_object.author #업데이트할 객체를 가져옴

class VideoDeleteView(DeleteView): # video_confirm_delete.html로 기본 템플릿명이며 post요청시에 삭제된다
    model = Video
    success_url = reverse_lazy('isu:video_list')
    def test_func(self):
        return self.request.user == self.get_object().author

   
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class =CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.video = get_object_or_404(Video, pk=self.kwargs['video_pk'])
        return super().form_valid(form)

        
     #성공url을 get_absolut_url 로 모델에 정의해도되지만 video_pk가필요해서 여기에서함
    def get_success_url(self):
        return resolve_url('isu:video_detail', self.kwargs['video_pk'])

class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return resolve_url('isu:video_detail', self.kwargs['video_pk']) # 여기서는 path.join처럼 주소를 합쳐줄뿐이고 함수형에서 return으로 바로 쓰지는못함



@login_required
def likeUpdate(request,pk):
    video = get_object_or_404(Video, pk=pk)

    if request.user in video.like.all():
        video.like.remove(request.user)
    else:
        video.like.add(request.user)
        
    return redirect('isu:video_detail', pk)