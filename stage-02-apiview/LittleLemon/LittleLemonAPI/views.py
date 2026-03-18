# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .selectors import get_all_menu_items
from .serializers import MenuItemsSerializer
from .models import MenuItem
from .permissions import is_manager

# Create your views here.

class MenuItemsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        menu_items = get_all_menu_items()
        serializer = MenuItemsSerializer(menu_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not is_manager(request.user):
            return Response({"error":"Only Manager can create a menu item"}, status=status.HTTP_403_FORBIDDEN)

        serializer = MenuItemsSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class MenuItemDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(MenuItem, pk =id)
    
    def get(self, request, id):
        menu_item = self.get_object(id)
        serializer = MenuItemsSerializer(menu_item)
        return Response(serializer.data)
    
    def put(self, request, id):
        if not is_manager(request.user):
            return Response({"error":"Only Manager can modify a menu item"}, status=status.HTTP_403_FORBIDDEN)

        menu_item = self.get_object(id)
        serializer = MenuItemsSerializer(menu_item, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        if not is_manager(request.user):
            return Response({"error":"Only Manager can modify a menu item"}, status=status.HTTP_403_FORBIDDEN)

        menu_item = self.get_object(id)
        serializer = MenuItemsSerializer(menu_item, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def delete(self, request, id):
        if not is_manager(request.user):
            return Response({"error":"Only Manager can delete a menu item"}, status=status.HTTP_403_FORBIDDEN)

        menu_item = self.get_object(id)
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




    
