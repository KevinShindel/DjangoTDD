from django.contrib import admin
from django.urls import path, include

from accounts.urls import accounts_urls
from lists.forms import ItemForm
from lists.urls import list_urls
from django.views.generic import FormView

urlpatterns = [
    path('', FormView.as_view(template_name='lists/home.html', form_class=ItemForm), name='home'),
    path('lists/', include(list_urls)),
    path('accounts/', include(accounts_urls)),
    path('admin/', admin.site.urls),
]
