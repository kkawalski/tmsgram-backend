from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from core.views import ProfileListView, SearchView, hello, ProfileDetailView, FollowView, UserRegisterView 


urlpatterns = [
    path("", hello),
    path("api/", include("core.api.urls")),
    path("profiles", ProfileListView.as_view(), name="profile_list"),
    path("profiles/<slug>", ProfileDetailView.as_view(), name="profile"),
    path("profiles/<slug>/follow", FollowView.as_view(), name="follow"),
    path("register", UserRegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("search", SearchView.as_view(), name="search"),
]
