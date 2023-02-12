"""Serializers приложения api."""
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Serializer для PostViewSet."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Fields заполнены по принципу: Явное лучше, чем неявное."""

        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для CommentViewSet."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Fields заполнены по принципу: Явное лучше, чем неявное."""

        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Serializer для GroupViewSet."""

    class Meta:
        """Fields заполнены по принципу: Явное лучше, чем неявное."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Serializer для FollowViewSet."""

    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        """Проверка, что нельзя User подписаться на себя."""
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

    class Meta:
        """Fields заполнены по принципу: Явное лучше, чем неявное."""

        model = Follow
        fields = ('user', 'following')
        read_only_fields = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Нельзя повторно подписаться на пользователя'
            )
        ]
