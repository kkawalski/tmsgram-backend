from django.urls import path, include

from posts.views import PostCreateView, PostDetailView, HashTagDetailView


urlpatterns = [
    path("posts/", PostCreateView.as_view(), name="post_list"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("search/hashtag/<str:slug>", HashTagDetailView.as_view(), name="hashtag"),
    path("api/", include("posts.api.urls"))
]
