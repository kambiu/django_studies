from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encrypt_key = models.CharField(max_length=256)
    retry_times = models.IntegerField(null=True, blank=True, default=0)

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#        profile, created = MyUser.objects.get_or_create(user=instance)

# post_save.connect(create_user_profile, sender=User)

class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    password = models.BinaryField()
    date_create = models.DateField()
    date_expire = models.DateField()
    remark = models.CharField(max_length=1000)
    order_id = models.IntegerField()

    def __str__(self):
        return self.username