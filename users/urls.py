from django.urls import path
from . import views


urlpatterns = [
    path('createuser/', views.ListCreateUser.as_view(), name='createuser'),
    path('login/', views.LoginView.as_view(), name='login'),
]