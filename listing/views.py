from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from .models import List
from .serializers import  ListSerializer


class ListViewSet(CreateModelMixin, 
                ListModelMixin, 
                UpdateModelMixin, 
                DestroyModelMixin, 
                GenericViewSet):

    http_method_names = ['post', 'get', 'patch', 'delete']
    
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = List.objects.all()
        else:
            queryset = List.objects.filter(user_id=user.id)
        return queryset

    def get_serializer_context(self):
        return {'user' : self.request.user}    

    def destroy(self, request, *args, **kwargs):
        is_soft = request.data.get('soft_delete', '1')
        if is_soft != '1':
            return super().destroy(request, *args, **kwargs)
        instance  = super().get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
