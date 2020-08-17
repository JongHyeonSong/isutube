from django.urls import path



from . import views

app_name = 'isu'
urlpatterns = [
    path('', views.VideoListView.as_view(), name='video_list'),
    path('new/', views.VideoCreateView.as_view(), name='video_create'),
    path('<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('<int:pk>/update/', views.VideoUpdateView.as_view(), name='video_update'),
    path('<int:pk>/delete/', views.VideoDeleteView.as_view(), name='video_delete'),

    path('<int:video_pk>/comment/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('<int:video_pk>/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('<int:pk>/like/update/', views.likeUpdate, name='like_update'),
]
