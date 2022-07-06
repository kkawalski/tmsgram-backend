from rest_framework import serializers

from core.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    password = serializers.CharField(required=True, write_only=True)
    password_submit = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_submit",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_submit"]:
            raise serializers.ValidationError("Passwords unmatched")
        return super().validate(attrs)

    def create(self, validated_data, **kwargs):
        validated_data.pop("password_submit")
        return User.objects.create_user(**validated_data)


class UserBaseSerializer(serializers.ModelSerializer):
    followed_by_me = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "followed_by_me",
            "is_active",
            "is_superuser",
        ]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_followed_by_me(self, obj):
        current_user = self.context["request"].user
        return obj in current_user.following.all()


from posts.api.serializers import PostBaseSerializer

class UserSerializer(UserBaseSerializer):
    total_following = serializers.SerializerMethodField(read_only=True)
    total_followers = serializers.SerializerMethodField(read_only=True)
    posts = PostBaseSerializer(read_only=True, many=True)

    class Meta(UserBaseSerializer.Meta):
        model = User
        fields = UserBaseSerializer.Meta.fields + [
            "posts",
            "total_following",
            "total_followers",
        ]

    def get_total_following(self, obj):
        return obj.following.count()

    def get_total_followers(self, obj):
        return obj.followers.count()
