from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Tag
from .serializers import TagSerializer
from .permissions import IsOwnerOrStaffUser, UserCanCreateOwnObject


# Create your views here.
class TagViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated, IsOwnerOrStaffUser, UserCanCreateOwnObject)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Tag.objects.all()
        else:
            return Tag.objects.filter(user=user.id)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(TagViewSet, self).get_serializer(*args, **kwargs)