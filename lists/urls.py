from django.urls import path

from lists.views import my_lists, NewListView, ViewAndAddToList

list_urls = [
    path('new', NewListView.as_view(), name='new_list'),
    path('<int:pk>/', ViewAndAddToList.as_view(), name='view_list'),
    path('users/<str:email>', my_lists, name='my_lists')
]
