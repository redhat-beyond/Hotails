from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
    path('homepage/', views.homepage, name='homepage'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html',
                                                redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout')
]
