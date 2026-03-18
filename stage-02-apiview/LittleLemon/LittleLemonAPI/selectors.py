# selectors.py
from .models import *

def get_all_menu_items():
    return MenuItem.objects.all()