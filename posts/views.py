import re
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from posts.forms import PostCreateForm
from posts.models import HashTag, Post


class PostDetailView(LoginRequiredMixin, UpdateView):
    template_name = "post_detail.html"
    model = Post
    form_class = PostCreateForm
    context_object_name = "post"

    def get_success_url(self) -> str:
        url = reverse_lazy("post_detail", kwargs={"pk": self.object.id})
        return url


class PostCreateView(LoginRequiredMixin, CreateView):
    queryset = Post.objects.select_related("user")
    form_class = PostCreateForm
    template_name = "post_list.html"
    success_url = reverse_lazy("post_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["posts"] = queryset.following(self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class HashTagDetailView(LoginRequiredMixin, DetailView):
    model = HashTag
    template_name = "hashtag.html"
    slug_field = "text"
    
