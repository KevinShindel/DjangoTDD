from django.urls import path

from lists.api.views import ListAPIView

api_urls = [
    path('lists/<int:list_id>', ListAPIView, name='api_list')
]