from django.urls import path
from . import views
app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.post_create, name='post_create'),

    # /posts/1/comment_create/
    # create되는 post의 id가 1이라는 뜻임
    # comment_create랑 delete는 새로운 템플릿으로 이동 안하기 때문에 /가 안붙나?
    path('<int:post_id>/comment_create', views.comment_create, name='comment_create'),
    
    path('<int:post_id>/update/', views.post_update, name='post_update'),

    # path('<int:post_id>/update', views.post_update, name='post_update') 랑 다름

    # /posts/1/comment_delete/
    path('<int:comment_id>/comment_delete', views.comment_delete, name='comment_delete'),

    #/posts/1/post_like/
    path('<int:post_id>/post_like', views.post_like, name="post_like"),

    #/posts/serarch/
    path("search/", views.search, name='post_search'),



]