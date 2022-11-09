from datetime import datetime
from django.db import models
from users.models import User


class TransactionManager(models.Manager):
    def create_transaction(self, amount, category, organisation, user, date=datetime.now(), description=''):
        transaction = self.model(
            amount=amount,
            category=category,
            organisation=organisation,
            user=user,
            date=date,
            description=description
        )
        transaction.save()
        return transaction

    def update_transaction(self, transaction, amount, category, organisation, description='', date=datetime.now()):
        transaction.amount = amount
        transaction.date = date,
        transaction.category = category
        transaction.organisation = organisation
        transaction.description = description
        transaction.save()
        return transaction

    def delete_transaction(self, transaction):
        transaction.delete()
        return transaction


class Transaction(models.Model):
    amount = models.FloatField()
    date = models.DateTimeField(default=datetime.now())
    category = models.CharField(max_length=40)
    organisation = models.CharField(max_length=40)
    description = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = TransactionManager()

    def __str__(self):
        return "_".join([str(self.amount), self.category, self.user.username])
