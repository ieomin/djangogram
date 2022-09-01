from rest_framework import serializers
from djangogram.users.models import User as user_model
from . import models

class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            "id",
            "username",
            "profile_photo",
        )

class CommentSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer()
    class Meta:
        model = models.Comment
        fields = (
            "id",
            "contents",
            "author",
        )

class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    author = FeedAuthorSerializer()
    class Meta:
        model = models.Post
        fields = (
            "id",
            "image",
            "caption",

            "author",
            # foreign key 이기 때문에 post요청으로 받은 게 아니지만 시리얼라이저에서는 사용 가능
            "comment_post",
            # Post가 아닌 Comment모델의 외래키 posts의 related_name을 사용하여 Comment 전체를 가져옴

            # 해당 두개의 필드는 위에서 다른 시리얼라이저를 통해 가져옴
            "image_likes",
        )
