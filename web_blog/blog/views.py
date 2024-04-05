from rest_framework import generics

import os
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from .serializer import TopicSerializer, PostSerializer

from .models import Topic, Post


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TopicListAPIView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class PostByTopicAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        topic_name = self.kwargs["topic_name"]
        return Post.objects.filter(topics__name=topic_name)


def ckeditor_upload(request):
    uploaded_file = request.FILES.get("upload")
    if uploaded_file:
        # Check if the file is an image
        if uploaded_file.content_type.startswith("image"):
            try:
                # Generate a unique filename
                filename = default_storage.get_available_name(
                    os.path.join(settings.MEDIA_ROOT, "ckeditor", uploaded_file.name)
                )
                path = default_storage.save(filename, ContentFile(uploaded_file.read()))
                url = default_storage.url(path)
                return JsonResponse({"url": url})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "Uploaded file is not an image"}, status=400)
    else:
        return JsonResponse({"error": "No file uploaded"}, status=400)
