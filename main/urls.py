from django.contrib import admin
from django.urls import path

from lists.views import home_page, view_list

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/один-единственный-список-в-мире/', view_list),
    path('admin/', admin.site.urls),
]
