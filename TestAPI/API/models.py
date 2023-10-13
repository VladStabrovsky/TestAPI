from django.db import models

# Create your models here.

class Users(models.Model):
    login = models.CharField(max_length=50)
    registration_date = models.DateField()

class Credits(models.Model):
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    issuance_date = models.DateField()
    return_date = models.DateField()
    actual_return_date = models.DateField(null=True)
    body = models.FloatField()
    percent = models.FloatField()

class Dictionary(models.Model):
    name = models.CharField(max_length=50)

class Plans(models.Model):
    period = models.DateField()
    sum = models.FloatField()
    category = models.ForeignKey(Dictionary, on_delete=models.PROTECT)

class Payments(models.Model):
    sum = models.FloatField()
    payment_date = models.DateField()
    credit = models.ForeignKey(Credits, on_delete=models.PROTECT)
    type = models.ForeignKey(Dictionary, on_delete=models.PROTECT)