
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post', views.new_post, name= 'new_post'),
    path('follow', views.follow, name='follow'),
    path('profile/<str:profile>', views.profile, name='profile'),
    path('following', views.following, name='following'),
    path('edit/<str:editw>', views.edit, name='edit')
]
