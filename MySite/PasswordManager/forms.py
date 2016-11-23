from django import forms


class AccountForm(forms.Form):
    acc_grp_id = forms.IntegerField(label='GroupID')
    acc_type = forms.CharField(label='Type', max_length=100, min_length=3)
    acc_name = forms.CharField(label='Username', max_length=100, min_length=3)
    acc_token = forms.CharField(label='Password', max_length=100, min_length=3)
    acc_exp_date = forms.DateField(label='Expiry Date')
    acc_remark = forms.CharField(label='Remark', max_length=100)

