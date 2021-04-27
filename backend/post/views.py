import uuid
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from slugify import slugify
from .models import Post
from .serializers import PostSerializer, PostSerializerWithComment
from .permissions import IsStaffUserOrReadOnly, IsOwnerOnly


class PostsViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsStaffUserOrReadOnly, IsOwnerOnly,)
    queryset = Post.objects.all().order_by("-id")
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == 'retrieve' and str(self.request.user) != "AnonymousUser":
            return PostSerializerWithComment
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, slug=slugify(
            self.request.data['title']+str(uuid.uuid4())))

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()