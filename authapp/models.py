from django.db import models
from django.conf import settings
# Create your models here.


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Transactions(models.Model):
    user_name = models.CharField(max_length=30)
    transaction_date = models.DateField()
    description = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    amount = models.FloatField()
    balance = models.FloatField()

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.user_name, self.transaction_date,self.description,self.type,self.amount,self.balance)

