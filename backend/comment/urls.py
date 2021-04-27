from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet
router = DefaultRouter()
router.register("", CommentViewSet)
app_name = 'comment'
urlpatterns = [
    path('', include(router.urls))
]
