from django.db import models
from django.contrib.auth.models import User


# User Wallet
class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=250000.00
    )

    def __str__(self):
        return self.user.username + "'s Wallet"


# Transaction History
class Transaction(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    transaction_type = models.CharField(
    max_length=30,
    default='Transfer'
    )

    recipient_name = models.CharField(max_length=100)

    bank_name = models.CharField(max_length=100)

    account_number = models.CharField(max_length=10)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        default='Successful'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient_name