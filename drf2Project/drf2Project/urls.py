from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth_token/", include("djoser.urls.authtoken")),
    path('api/transactions/', include("transactions.urls")),
    path('api/', include("users.urls"))
]
