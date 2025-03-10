from django.contrib import admin
from django.urls import path, include
from league.views import home  # Import homepage view from league

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Add this line to handle the root URL
    path('api/', include('league.urls')),  # Your existing API URL pattern
]