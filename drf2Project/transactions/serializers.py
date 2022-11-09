from rest_framework import serializers

from transactions.models import Transaction


class TransactionDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = "__all__"
