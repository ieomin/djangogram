from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from djangogram.users.models import User as user_model
from . import models, serializers
from .forms import CreatePostForm, CommentForm, UpdatePostForm
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                Q (author__in=following) | Q(author=user)
            ).order_by("-create_at")
            # filter에는 하나의 조건만 넣을 수 있는데 Q객체를 사용해 or를 사용함
            # __in 은 여러 데이터를 허용함

            serializer = serializers.PostSerializer(posts, many=True)

            return render(request, 
            'posts/main.html', 
            {'posts':serializer.data, "comment_form":comment_form})

def post_create(request):
    if request.method == 'GET':
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {"form": form}) 

    elif request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # 포스트를 생성할 때 어떤 유저가 만든지 알기 위해 필요해서 user.id를
            # 이용해 user 객체를 가져옴

            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )

            # new_post.save() 
            # 아까는 Signup폼 받아서 저장해주더니 이번엔 Post 모델을 저장

            form = CreatePostForm(request.POST, request.FILES)

            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                # foreign key 이기 때문에 post요청으로 받은 게 아님
                form.save()

            else:
                print(form.errors)

            return redirect(reverse('posts:index'))

        else:
            return render(request, 'users/main.html')

def comment_create(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            # form과 유효성 검사와 저장은 한 세트
            comment = form.save(commit=False)
            comment.author = request.user
            comment.posts = post
            comment.save()

            return redirect(reverse('posts:index') + "#comment-" + str(comment.id))
        else:
            return render(request, 'users/main.html')


def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()

        return redirect(reverse('posts:index'))
    else:
        return render(request, 'users/main.html')

def post_update(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user != post.author:
            return redirect(reverse('posts:index'))

        if request.method == 'GET':
            
            form = UpdatePostForm(instance=post)
            # 전에 작성된 것을 보여주기 위함
            
            return render(request, 
                'posts/post_update.html', 
                {"form": form, "post":post}
                )
        
        elif request.method == 'POST':
            post = get_object_or_404(models.Post, pk=post_id)

            form = UpdatePostForm(request.POST)

            if form.is_valid():
                post.caption = form.cleaned_data['caption']
                post.save()

                # form.save() 수정할 땐 이렇게 하면 안됨 수정은 폼을 이용하기만 함

            return redirect(reverse('posts:index'))
    else:
        return render(request, 'users/main.html')


def post_like(request, post_id):
    response_body = {"result": ""}
    # result는 내가 정한 비어있는 변수

    if request.user.is_authenticated:
        if request.method == "POST":

            post = get_object_or_404(models.Post, pk=post_id)
            existed_user = post.image_likes.filter(pk=request.user.id).exists()
            # image_likes는 유저모델
            if existed_user:
                # 좋아요 취소가 되야 함
                post.image_likes.remove(request.user)
                response_body["result"] = "dislike"
            else:
                # 좋아요가 되야함
                post.image_likes.add(request.user)
                response_body["result"] = "like"

                
            post.save()
            return JsonResponse(status=200, data=response_body)
    else:
        return JsonResponse(status=403, data=response_body)
        # 403은 권한이 없다는 상태
def search(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            searchKeyword = request.GET.get("q", "")

            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                (Q (author__in=following) | Q(author=user)) & Q(caption__contains=searchKeyword)
            ).order_by("-create_at")

            serializer = serializers.PostSerializer(posts, many=True)

            return render(request, 
            'posts/main.html', 
            {'posts':serializer.data, "comment_form":comment_form})
    else:
        return render(request, 'users/main.html')