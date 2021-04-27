from collections import OrderedDict
from comment.models import Comment
from rest_framework import serializers
from .models import Post
from category.models import Category
from category.serializers import CategorySerializer
from tag.models import Tag
from tag.serializers import TagSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


class ModifiedRelatedField(serializers.RelatedField):
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        if cutoff is not None:
            queryset = queryset[:cutoff]
        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])


class CategoryField(ModifiedRelatedField):
    def to_representation(self, value):
        return CategorySerializer(value).data

    def to_internal_value(self, value):
        try:
            try:
                return Category.objects.get(id=value)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Obj does not exist.'
            )


class TagField(ModifiedRelatedField):
    def to_representation(self, value):
        return TagSerializer(value).data

    def to_internal_value(self, value):
        if isinstance(value, dict) and len(value) > 0:
            if not value.get('user', False):
                raise serializers.ValidationError(
                    'Invalid tag data.'
                )
            try:
                user = get_user_model().objects.get(id=value.get('user', ''))
                value['user'] = user.id
                serializer = TagSerializer(data=value)
                if serializer.is_valid(raise_exception=True):
                    new_tag = serializer.save()
                    return new_tag
                else:
                    raise serializers.ValidationError(
                        'Invalid tag data.'
                    )
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    'User in tag does not exist.'
                )
        if isinstance(value, (str, int)):
            try:
                return Tag.objects.get(id=value)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    'Obj does not exist.'
                )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('id', 'username', 'password', 'first_name',
        #           'last_name', 'email', 'date_joined', 'about', 'image', 'phone_num')
        fields = ('id', 'username', 'image', 'first_name',
                  'last_name', )  # i just need these infos
        extra_kwargs = {"password": {"write_only": True, 'required': True}}


class PostSerializer(serializers.ModelSerializer):
    category = CategoryField(queryset=Category.objects.all(), required=False)
    tags = TagField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('id', 'author', 'slug',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = UserSerializer(instance.author).data
        return response


class PostSerializerWithComment(serializers.ModelSerializer):

    category = CategoryField(queryset=Category.objects.all(), required=False)
    tags = TagField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('id', 'slug', 'comments_list')

    def to_representation(self, instance):
        from comment.serializers import CommentSerializer

        response = super().to_representation(instance)
        comments_objects_list = Comment.objects.filter(post=instance.id)
        comments_list = []
        for i in comments_objects_list:
            serializer = CommentSerializer(i)
            comments_list.append(serializer.data)
        response['comments_list'] = comments_list
        response['author'] = UserSerializer(instance.author).data
        return response