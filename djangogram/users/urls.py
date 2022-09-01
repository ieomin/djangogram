from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('', views.main, name='main'),
    # include("djangogram.users.urls", namespace="users") ->
    # views.main, name='main
    path('signup', views.signup, name='signup'),
    
]
