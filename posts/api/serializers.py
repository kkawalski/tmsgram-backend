from rest_framework import serializers

from core.api.serializers import UserBaseSerializer
from posts.models import Post


class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "description",
            "image",
            "is_active",
        ]


class PostSerializer(PostBaseSerializer):
    user = UserBaseSerializer(default=serializers.CurrentUserDefault())
    
    class Meta(PostBaseSerializer.Meta):
        fields = PostBaseSerializer.Meta.fields + [
            "user",
        ]
