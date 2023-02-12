"""Views приложения api."""
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from posts.models import Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet модели Post."""

    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group', )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Автозаполнения поля author."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet
                    ):
    """ViewSet модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        """Автозаполнения поля author."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Queryset Для FollowViewSet."""
        return Follow.objects.select_related(
            'user',
            'following'
        ).filter(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_post(self):
        """Получаем Post."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post

    def get_queryset(self):
        """Queryset для CommentViewSet."""
        post = self.get_post()
        queryset = post.comments.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        """Автозаполнения поля author и post."""
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
