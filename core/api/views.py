import threading
from rest_framework import viewsets, status, filters, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.serializers import UserBaseSerializer, UserSerializer, RegisterSerializer
from core.models import User


class UserViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet,
    ):
    queryset = User.objects
    serializer_class = UserBaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        "register": [permissions.AllowAny,],
        "activate": [permissions.AllowAny,]
    }
    search_fields = ["username"]
    ordering_fields = ["created_at", "id"]

    def get_queryset(self):
        queryset = self.queryset.exclude(id=self.request.user.id)
        if self.action in ("retrieve",):
            queryset = queryset.prefetch_related("posts")
        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        if self.action in self.permission_classes_by_action:
            permissions = self.permission_classes_by_action[self.action]
        else:
            permissions = self.permission_classes
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action in ("retrieve", "me"):
            return UserSerializer
        elif self.action == "register":
            return RegisterSerializer
        return self.serializer_class

    @action(methods=["GET"], detail=True)
    def followed_by(self, request, pk=None):
        user = self.get_object()
        current_user = request.user
        followers = user.followers.filter(id__in=current_user.following.values_list("id", flat=True))
        res_data = self.get_serializer(instance=followers, many=True).data
        return Response(res_data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.followers
        res_data = self.get_serializer(instance=followers, many=True).data
        return Response(res_data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()
        res_data = self.get_serializer(instance=following, many=True).data
        return Response(res_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def register(self, request):
        register_data = request.data
        serializer_obj = self.get_serializer(data=register_data)
        serializer_obj.is_valid(raise_exception=True)
        user = serializer_obj.save()
        user.is_active = False
        user.save()
        user.send_register_mail()
        return Response(serializer_obj.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False)
    def activate(self, request):
        register_token = request.data.get("register_token")
        user = User.activate(register_token)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def follow(self, request, pk=None):
        user = self.get_object()
        current_user = request.user
        if user in current_user.following.all():
            current_user.following.remove(user)
        else:
            current_user.following.add(user)
        current_user.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    
    @action(methods=["GET", "PUT", "DELETE"], detail=False)
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serialized_user = self.get_serializer(instance=user)
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        if request.method == "PUT":
            serialized_user = self.get_serializer(instance=user, data=request.data, partial=True)
            serialized_user.is_valid(raise_exception=True)
            serialized_user.save()
            return Response(serialized_user.data, status=status.HTTP_202_ACCEPTED)
        if request.method == "DELETE":
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
