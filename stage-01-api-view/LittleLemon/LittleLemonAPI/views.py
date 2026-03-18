# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import MenuItem
from .serializers import MenuItemSerializer
from .selectors import get_menu_item_by_id


# Create your views here.

@api_view(['GET','POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        if not request.user.groups.filter(name = "Manager").exists():
            return Response(
                {"error":"Only Manager can create menu items"}, 
                status=status.HTTP_403_FORBIDDEN
            )
    
        serializer = MenuItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
@api_view(['GET','PUT','PATCH','DELETE'])
def menu_item_detail(request, id):

    # Only Manager are allowed PUT, PATCH, DELETE
    if request.method in ['PUT','PATCH','DELETE']:
        if not request.user.groups.filter(name = "Manager").exists():
            return Response(
                {"error":"Only managers can modify menu items"}, 
                status=status.HTTP_403_FORBIDDEN
            )

    item = get_menu_item_by_id(id)

    if request.method == 'GET':
        serializer = MenuItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = MenuItemSerializer(item, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method =='PATCH':
        serializer = MenuItemSerializer(item, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()    
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)