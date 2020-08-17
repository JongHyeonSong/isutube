from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name="login"),
    path('logout/', views.LogoutPageView.as_view(), name="logout"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('profile/', views.profile, name="profile"),
]