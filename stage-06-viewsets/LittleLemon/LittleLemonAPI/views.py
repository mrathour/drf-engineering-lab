# views.py

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsManagerOrReadOnly

# Create your views here.


class MenuItemViewSet(GenericViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['featured']
    ordering_fields = ['price','inventory']

    def list(self, request):
        menu_items = self.get_queryset()
        menu_items = self.filter_queryset(menu_items)
        page = self.paginate_queryset(menu_items)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)        

    def retrieve(self, request, pk):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item)
        return Response(serializer.data)

    def update(self, request, pk):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item, data= request.data, partial= True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        menu_item = self.get_object()
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


