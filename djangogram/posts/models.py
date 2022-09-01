from email.mime import image
from tkinter import N
from django.db import models
from djangogram.users import models as user_model # 이건 절대 경로

# Create your models here.

class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True # 단독 생성 방지


class Post(TimeStamedModel):
    author = models.ForeignKey(user_model.User,
        null=True,
        on_delete=models.CASCADE, # 의존하는 User행이 삭제 되었을 때 같이 삭제
        related_name='post_author'
        )

    image = models.ImageField(blank=False)
    # blank가 꼭 들어가야 한다는 의미이고 null은 NULL값이 들어갈 수 있다는 의미
    caption = models.TextField(blank=False)
    image_likes = models.ManyToManyField(
        user_model.User, 
        related_name='post_image_likes',
        blank=True
        )

    def __str__(self):
        return f"{self.author}: {self.caption}"


class Comment(TimeStamedModel):

    author = models.ForeignKey(user_model.User,
        null=True,
        on_delete=models.CASCADE, # 의존하는 User 모델이 삭제 되었을 때 같이 삭제
        related_name='comment_author' # 뒤에 것이 의존되는 모델
        )
    
    posts = models.ForeignKey(Post,
        null=True,
        on_delete=models.CASCADE, # 의존하는 User 모델이 삭제 되었을 때 같이 삭제
        related_name='comment_post'
        )

    contents = models.TextField(blank=True)

    def __str__(self):
        return f"{self.author}: {self.contents}"
