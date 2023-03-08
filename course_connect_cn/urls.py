from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('apis/', include('apis.urls')),
    path('ping/', include('ping.urls')),
    path('scheduler/', include('schd.urls')),
    path('admin/', admin.site.urls),
]
