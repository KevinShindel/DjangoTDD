from django.contrib import admin
from django.urls import path, include

from lists.urls import list_patterns
from lists.views import home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/', include(list_patterns)),
    path('admin/', admin.site.urls),
]
