from django.shortcuts import render_to_response, render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Group, Account
from .forms import AccountForm
import datetime
from PasswordManager import common
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout


def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('pm:index'))


def login_page(request):
    return render(request, "pm/login.html")


def login_request(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        print("Return login")
        return HttpResponseRedirect(reverse('pm:index'))
    else:
        return HttpResponseNotFound('<h1>User not found</h1>')

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pm:group-list'))
    else:
        return HttpResponseRedirect(reverse('pm:login'))


class GroupListView(generic.ListView):

    template_name = 'pm/group_list.html'
    context_object_name = "all_groups"

    def get_queryset(self):
        return Group.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user.username
        return context


class GroupDetailView(generic.DetailView):
    model = Group  # this only work for url pass in parameters
    template_name = 'pm/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
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
        account_id = request.GET['acc_id']
        binary_password = Account.objects.get(pk=account_id).password
        login_password = "admin"
        hashed_key = common.get_key(login_password)
        token_display = common.decrypt(hashed_key, binary_password)
        return HttpResponse(token_display)
    else:
        return HttpResponse("Error made.")


def account_create(request):

    if request.method == 'POST':
        form = AccountForm(request.POST)

        create_date = datetime.datetime.now().strftime("%Y-%m-%d")
        order_id = 0  # default to zero first
        login_password = "admin"
        hashed_key = common.get_key(login_password)

        if form.is_valid():
            acc_group_id = form.cleaned_data['acc_grp_id']
            acc_group = Group.objects.get(pk=acc_group_id)
            new_account = Account()
            new_account.Group = acc_group
            new_account.group_id = acc_group_id
            new_account.type = form.cleaned_data['acc_type']
            new_account.username = form.cleaned_data['acc_name']
            binary_token = common.encrypt(hashed_key, form.cleaned_data['acc_token'])
            new_account.password = binary_token
            new_account.date_create = create_date
            new_account.date_expire = form.cleaned_data['acc_exp_date']
            new_account.remark = form.cleaned_data['acc_remark']
            new_account.order_id = order_id
            new_account.save()
        else:
            print(form.errors)
    else:
        form = AccountForm()

    return HttpResponseRedirect(reverse('pm:group-detail', args=(acc_group_id,)))


def account_update(request, account_id):

    if request.method == 'POST':
        form = AccountForm(request.POST)
        login_password = "admin"
        hashed_key = common.get_key(login_password)

        if form.is_valid():
            update_account = Account.objects.get(pk=account_id)
            update_account.type = form.cleaned_data['acc_type']
            update_account.username = form.cleaned_data['acc_name']
            binary_token = common.encrypt(hashed_key, form.cleaned_data['acc_token'])
            update_account.password = binary_token
            update_account.date_expire = form.cleaned_data['acc_exp_date']
            update_account.remark = form.cleaned_data['acc_remark']
            update_account.save()
        else:

            print(form.errors)
    else:
        form = AccountForm()

    return HttpResponseRedirect(reverse('pm:group-detail', args=(update_account.group_id,)))


def account_details(request):
    if request.method == 'GET':
        account_id = request.GET['acc_id']
        retrieving_account = Account.objects.get(pk=account_id)
        dict_details = {}
        dict_details['acc_type'] = retrieving_account.type
        dict_details['acc_name'] = retrieving_account.username
        # password
        login_password = "admin"
        hashed_key = common.get_key(login_password)
        token_display = common.decrypt(hashed_key, retrieving_account.password)
        dict_details['acc_token'] = token_display

        dict_details['acc_exp_date'] = retrieving_account.date_expire.strftime('%Y-%m-%d')
        dict_details['acc_remark'] = retrieving_account.remark

        return HttpResponse(json.dumps(dict_details))
    else:
        return HttpResponse("Error made.")
    # return render_to_response('pm/group_detail.html', {'token': str(token_id) + " added"})
