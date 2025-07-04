
from django.db import models
from user.models import Users

class Transaction(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=100)
    amount = models.FloatField()
    debit = models.FloatField(null=True, blank=True)
    credit = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_fraud = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    #remark=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

class FraudData(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    fraud_type = models.CharField(max_length=100)
    fraud_description = models.TextField()

    def __str__(self):
        return self.fraud_type

class FraudAccount(models.Model):
    account_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.account_number
