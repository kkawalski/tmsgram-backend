from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from posts.models import Post
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_superuser:
            queryset = queryset.filter_is_active()
        print(queryset.filter(user=self.request.user).all())
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print("LIST QUERY", queryset.values("user", "description")[:5])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print("SERIALIZER DATA", serializer.data[:5])
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        post.is_active = False
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)