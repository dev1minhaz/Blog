from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer
from .permissions import OwnerCanUpdateOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (OwnerCanUpdateOrReadOnly, IsAuthenticated)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['depth'] = self.request.query_params.get('depth', 1)
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
