from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'


class BankAccount(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.owner.username

    def deposit(self, amount):
        self.balance += amount
        self.save()
        Transaction.objects.create(account=self, transaction_type='Deposit', amount=amount)

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            Transaction.objects.create(account=self, transaction_type='Withdraw', amount=amount)
            return True
        return False

    class Meta:
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
    )
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='Deposit')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date']
