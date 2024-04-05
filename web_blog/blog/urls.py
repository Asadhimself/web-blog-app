from django.urls import path

from .views import (
    PostByTopicAPIView,
    PostDetailApiView,
    PostListCreateAPIView,
    TopicListAPIView,
)

urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetailApiView.as_view(), name="post-detail"),
    path("topics/", TopicListAPIView.as_view(), name="category-list"),
    path(
        "topics/<str:topic_name>/",
        PostByTopicAPIView.as_view(),
        name="posts-by-category",
    ),
]
