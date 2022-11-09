from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CategoryViewSet, UserView

router = DefaultRouter()
router.register(r'', CategoryViewSet, basename='category')


urlpatterns = [
    path('me/', UserView.as_view()),
    path("categories/", include(router.urls))
]
