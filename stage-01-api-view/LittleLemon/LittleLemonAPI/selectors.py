# selectors.py
from django.shortcuts import get_object_or_404
from .models import MenuItem

def get_menu_item_by_id(item_id):
    return get_object_or_404(MenuItem, pk=item_id)
