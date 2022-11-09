from rest_framework.permissions import IsAuthenticated
from transactions.permissions import IsOwner
from transactions.models import Transaction
from transactions.serializers import TransactionDetailSerializer
from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from transactions.filters import TransactionFilter
from users.models import Category, UserProfile
from rest_framework import exceptions


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionDetailSerializer
    permission_classes = (IsOwner, IsAuthenticated)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = TransactionDetailSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=False)
        current_category = serializer.validated_data['category']
        user_categories = Category.objects.filter(user=self.request.user).values_list('category', flat=True)
        if current_category in user_categories:
            money = serializer.validated_data['amount']
            if current_category == "Зарплата":
                money = -money
            cur_balance = UserProfile.objects.get(user=self.request.user).balance
            if cur_balance - money < 0:
                raise exceptions.ValidationError("not enougn balance")
            else:
                UserProfile.objects.update(balance=cur_balance-money)
            return super().create(request, args, kwargs)
        else:
            raise exceptions.ValidationError("No such category")

    def update(self, request, *args, **kwargs):
        serializer = TransactionDetailSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=False)
        new_category = serializer.validated_data['category']
        new_amount = serializer.validated_data['amount']
        user_categories = Category.objects.filter(user=self.request.user).values_list('category', flat=True)
        if new_category in user_categories:
            cur_user = UserProfile.objects.get(user=self.request.user)
            old_transaction = Transaction.objects.get(id=kwargs['pk'])
            cur_balance = cur_user.balance
            old_category = old_transaction.category
            old_amount = old_transaction.amount
            if new_category == "Зарплата":
                new_amount = -new_amount
            if old_category == "Зарплата":
                old_amount = -old_amount
            if cur_balance + old_amount - new_amount < 0:
                raise exceptions.ValidationError("not enougn balance")
            else:
                UserProfile.objects.update(balance=cur_balance + old_amount - new_amount)
            return super().update(request, args, kwargs)
        else:
            raise exceptions.ValidationError("No such category")


class SortedTransactionListView(generics.ListAPIView):
    serializer_class = TransactionDetailSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by(self.kwargs['col'])
