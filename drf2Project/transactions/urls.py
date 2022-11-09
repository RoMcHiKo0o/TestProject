from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions.views import TransactionViewSet, SortedTransactionListView

router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('sortby/<str:col>/', SortedTransactionListView.as_view())
]
