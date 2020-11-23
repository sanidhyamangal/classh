from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename="posts")
router.register(r'comments', views.CommentViewSet, basename="comments")
urlpatterns = [
    path('', include(router.urls)),
]
