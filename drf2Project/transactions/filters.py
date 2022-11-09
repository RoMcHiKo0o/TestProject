from django_filters import rest_framework as filters

from transactions.models import Transaction


class TransactionFilter(filters.FilterSet):
    amount = filters.RangeFilter()
    date = filters.DateTimeFromToRangeFilter()
    categories = filters.CharFilter(field_name='category')
    organisations = filters.CharFilter(field_name='organisation')

    class Meta:
        model = Transaction
        fields = ('amount', 'date', 'category', 'organisation')
