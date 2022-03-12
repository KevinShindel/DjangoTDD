from django.contrib import admin
from django.urls import path, include

from accounts.urls import accounts_urls
from lists.urls import list_urls
from lists.views import home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/', include(list_urls)),
    path('accounts/', include(accounts_urls)),
    path('admin/', admin.site.urls),
]
