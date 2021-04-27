from rest_framework import serializers
from .models import Comment
from post.serializers import UserSerializer
from collections import OrderedDict


class ModifiedRelatedField(serializers.RelatedField):
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        if cutoff is not None:
            queryset = queryset[:cutoff]
        return OrderedDict([(item.pk, self.display_value(item)) for item in queryset])


class CommentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        context = kwargs.get("context")
        if context is not None:
            depth = context.get("depth")
            if depth in ['1', '2']:
                self.Meta.depth = int(depth)
        super(CommentSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'post')
        read_only_fields = ('id', 'user')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response