from django.shortcuts import render
from featureflags.client import CfClient
from featureflags.evaluations.auth_target import Target
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Post
from .serializers import PostSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

api_key = "e478ef59-12a1-468f-aab6-db48b6fd8e90"
cf = CfClient(api_key)
cf.wait_for_initialization()

def is_feature_enabled(flag_key, target_identifier, target_name, default=False):
    target = Target(identifier=target_identifier, name=target_name)
    return cf.bool_variation(flag_key, target, default)

feature_enabled =is_feature_enabled('crud', 'target1', 'Django_crud', False)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        if not is_feature_enabled('crud', 'target1', 'Django_crud', False):
            raise PermissionDenied("CRUD operations are disabled")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not is_feature_enabled('crud', 'target1', 'Django_crud', False):
            raise PermissionDenied("CRUD operations are disabled")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not is_feature_enabled('crud', 'target1', 'Django_crud', False):
            raise PermissionDenied("CRUD operations are disabled")
        return super().destroy(request, *args, **kwargs)

@csrf_exempt
def feature_flag_view(request):
    return JsonResponse({'feature_enabled': feature_enabled})
