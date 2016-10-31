from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=250)
    date_create = models.DateField()
    remark = models.CharField(max_length=1000)
    order_id = models.IntegerField()

    def __str__(self):
        return self.name


class Account(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    type = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    date_create = models.DateField()
    date_expire = models.DateField()
    remark = models.CharField(max_length=1000)
    order_id = models.IntegerField()

    def __str__(self):
        return self.username