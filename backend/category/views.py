from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.authentication import TokenAuthentication
from .models import Category
from .serializers import CategorySerializer
from .permissions import IsStaffUserOrReadOnly


class CategoryViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsStaffUserOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
