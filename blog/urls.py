from django.urls import include, path
from rest_framework import routers
from .views import PostViewSet , feature_flag_view

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")

urlpatterns = [
    path('', include(router.urls)),
    path('feature-flag/', feature_flag_view, name='feature-flag'),
]
