from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'user')
        read_only_fields = ('id',)

    def create(self, validated_data):
        tag, created = Tag.objects.get_or_create(**validated_data)
        return tag
