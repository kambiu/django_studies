from django import forms
from django.forms import ModelForm
from .models import MyUser
from django.contrib.auth.models import User


class AccountForm(forms.Form):
    acc_grp_id = forms.IntegerField(label='GroupID')
    acc_type = forms.CharField(label='Type', max_length=100, min_length=3)
    acc_name = forms.CharField(label='Username', max_length=100, min_length=3)
    acc_token = forms.CharField(label='Password', max_length=100, min_length=3)
    acc_exp_date = forms.DateField(label='Expiry Date')
    acc_remark = forms.CharField(label='Remark', max_length=100)


class GroupForm(forms.Form):
    gp_user_id = forms.CharField(label='User', max_length=100, min_length=3)
    gp_name = forms.CharField(label='Grou Name', max_length=100, min_length=3)
    gp_remark = forms.CharField(label='Remark', max_length=100, min_length=3)
    gp_order = forms.IntegerField(label="OrderId")


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class UserProfileForm(ModelForm):
    class Meta:
        model = MyUser
        exclude = ['user']