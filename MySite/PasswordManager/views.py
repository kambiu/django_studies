from django.shortcuts import render_to_response
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Group, Account
from .forms import AccountForm
import datetime

class IndexView(generic.ListView):
    template_name = 'pm/index.html'
    context_object_name = "all_groups"

    def get_queryset(self):
        return Group.objects.all()


class GroupDetailView(generic.DetailView):
    model = Group  # this only work for url pass in parameters
    template_name = 'pm/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['now'] = "111"
        return context


class GroupCreate(CreateView):
    template_name = "pm/group_template.html"
    model = Group
    fields = ['name', 'date_create', 'remark', 'order_id']
    success_url = reverse_lazy("pm:index")


class GroupUpdate(UpdateView):
    template_name = "pm/group_template.html"
    model = Group
    fields = ['name', 'date_create', 'remark', 'order_id']
    success_url = reverse_lazy("pm:index")


class GroupDelete(DeleteView):
    template_name = "pm/group_template.html"
    model = Group
    success_url = reverse_lazy("pm:index")


def token(request):
    if request.method == 'GET':
        token_id = request.GET['test_id']
        all_acounts = Account.objects.all().filter(id=token_id)
        print (all_acounts[0].password)
        return HttpResponse("Password is: " + all_acounts[0].password)
    else:
        return HttpResponse("Error made.")
    # return render_to_response('pm/group_detail.html', {'token': str(token_id) + " added"})


def account_create(request):

    if request.method == 'POST':
        print("account_create() - Form Post")
        form = AccountForm(request.POST)

        create_date = datetime.datetime.now().strftime("%Y-%m-%d")
        order_id = 0  # default to zero first
        if form.is_valid():
            acc_group_id = form.cleaned_data['acc_grp_id']
            acc_group = Group.objects.get(pk=acc_group_id)
            new_account = Account()
            new_account.Group = acc_group
            new_account.type = form.cleaned_data['acc_type']
            new_account.username = form.cleaned_data['acc_name']
            new_account.password = form.cleaned_data['acc_token']
            new_account.date_create = create_date
            new_account.date_expire = form.cleaned_data['acc_exp_date']
            new_account.remark = form.cleaned_data['acc_remark']
            new_account.order_id = order_id
            new_account.save()
            print("account_create() - account is saved")

        else:
            print ("account_create() - Form Not Valid")
            print(form.errors)
    else:
        form = AccountForm()

    return HttpResponseRedirect('pm:index')
    # return HttpResponseRedirect('pm:group-detail')