# serializers.py
from rest_framework import serializers
from .models import *

class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
