from rest_framework.permissions import IsAuthenticated
from transactions.models import Transaction
from transactions.permissions import IsOwner
from rest_framework import viewsets, generics
from users.models import Category
from users.serializers import CategoryDetailSerializer, UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryDetailSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        for transaction in Transaction.objects.filter(user=request.user):
            if transaction.category == Category.objects.get(id=kwargs['pk']).category:
                transaction.category = self.request.data['category']
                transaction.save()

        return super().update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        for transaction in Transaction.objects.filter(user=request.user):
            if transaction.category == Category.objects.get(id=kwargs['pk']).category:
                transaction.delete()

        return super().destroy(request, args, kwargs)


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
