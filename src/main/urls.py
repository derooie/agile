from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('retrospectives/', include('retrospectives.urls', namespace='retrospectives')),
    path('', include('retrospectives.urls', namespace='index')),
]
