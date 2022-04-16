from django.contrib import admin
from django.urls import path, include

from accounts.urls import accounts_urls
from lists.api.urls import api_urls
from lists.urls import list_urls
from lists.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('lists/', include(list_urls)),
    path('accounts/', include(accounts_urls)),
    path('api/', include(api_urls)),
    path('admin/', admin.site.urls),
]
