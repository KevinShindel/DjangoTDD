from django.urls import path

from lists.views import new_list, view_list, add_item

list_patterns = [
    path('new', new_list),
    path('<int:list_id>/', view_list, name='view_list'),
    path('<int:list_id>/add_item', add_item, name='add_item'),
]