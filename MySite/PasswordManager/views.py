from django.shortcuts import render_to_response, render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Group, Account, MyUser, User
from .forms import AccountForm, UserForm, UserProfileForm, GroupForm
import datetime
from PasswordManager import common
import json
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('pm:index'))


def login_page(request):
    return render(request, "pm/login.html")


def login_request(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    attempt_user = User.objects.get(username=username)
    attempt_my_user = MyUser.objects.get(user_id=attempt_user.id)
    # print(attempt_my_user.retry_times)

    if attempt_my_user.retry_times >= 3:
        attempt_user.is_active = False
        attempt_user.save()
        return HttpResponseNotFound('<h1>This account is disabled</h1>')

    if user is not None:
        login(request, user)
        attempt_my_user.retry_times = 0
        attempt_my_user.save()
        return HttpResponseRedirect(reverse('pm:index'))
    else:
        attempt_my_user.retry_times += 1
        attempt_my_user.save()
        return HttpResponseNotFound('<h1>User not found</h1>')

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pm:group-list'))
    else:
        return HttpResponseRedirect(reverse('pm:login'))

@method_decorator(login_required, name='dispatch')
class GroupListView(generic.ListView):

    template_name = 'pm/group_list.html'
    context_object_name = "all_groups"

    def get_queryset(self):
        return Group.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user.username
        context['uid'] = self.request.user.pk
        return context

@method_decorator(login_required, name='dispatch')
class GroupDetailView(generic.DetailView):
    model = Group  # this only work for url pass in parameters
    template_name = 'pm/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context

@method_decorator(login_required, name='dispatch')
class GroupCreate(CreateView):
    template_name = "pm/group_template.html"
    model = Group
    fields = ['name', 'date_create', 'remark', 'order_id', 'user']
    success_url = reverse_lazy("pm:index")

    def get_context_data(self, **kwargs):
        context = super(GroupCreate, self).get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)

        create_date = datetime.datetime.now().strftime("%Y-%m-%d")
       
        if form.is_valid():
            gp_user_id = form.cleaned_data['gp_user_id']
            user = User.objects.get(username=gp_user_id)
            
            new_group = Group()
            new_group.user = user            
            new_group.name = form.cleaned_data['gp_name']
            new_group.date_create = create_date
            new_group.remark = form.cleaned_data['gp_remark']
            new_group.order_id = form.cleaned_data['gp_order']
            new_group.save()
        else:
            print("Check the following errors ...")
            print(form.errors)
    else:
        form = GroupForm()

    return HttpResponseRedirect(reverse('pm:group-list'))

@login_required
def group_delete(request):
    print("Enter group delete")

    if request.method == 'POST':
        pass
    else:
        pass

    return HttpResponseRedirect(reverse('pm:group-list'))

@method_decorator(login_required, name='dispatch')
class GroupUpdate(UpdateView):
    template_name = "pm/group_template.html"
    model = Group
    fields = ['name', 'date_create', 'remark', 'order_id']
    success_url = reverse_lazy("pm:index")


@method_decorator(login_required, name='dispatch')
class GroupDelete(DeleteView):
    template_name = "pm/group_template.html"
    model = Group
    success_url = reverse_lazy("pm:index")

@login_required
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

@login_required
def account_create(request):
    redirect_page_arg = 0
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
            redirect_page_arg = acc_group_id
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

    return HttpResponseRedirect(reverse('pm:group-detail', args=(redirect_page_arg,)))

@login_required
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

@login_required
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
    return render_to_response('pm/group_detail.html', {'token': str(token_id) + " added"})

@login_required
def account_delete(request):
    user_id = ""
    acc_id = ""
    if request.method == "POST":
        user_id = request.POST['user_id']
        acc_id = request.POST['acc_id']

    to_delete_account = Account.objects.get(id=acc_id)
    related_group = Group.objects.get(id=to_delete_account.group.id)
    related_user = User.objects.get(id=related_group.user.id)

    if int(related_user.id) == int(user_id):
        print("pending delete, confirmed user")
        to_delete_account.delete()
    else:
        print("Cannot delete user by this way")

    return HttpResponseRedirect(reverse('pm:group-detail', args=(related_group.id,)))


@method_decorator(login_required, name='dispatch')
class UserListView(generic.ListView):
    template_name = 'pm/user_list.html'
    context_object_name = "all_users"

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['name'] = "123"
        return context


@method_decorator(login_required, name='dispatch')
class UserCreate(CreateView):
    template_name = "pm/user_form.html"
    model = User
    fields = ['username', 'password']
    # fields = ['username', 'password', "encrypt_key"]
    success_url = reverse_lazy("pm:index")


@login_required
def change_key(request):
    context = dict()
    context["user_name"] = request.user
    u = User.objects.get(username=request.user)
    print(u)
    print(u.myuser.encrypt_key)
    context["user_key"] = User.objects.get(username=request.user).myuser.encrypt_key
    return render_to_response('pm/key.html', context)


def test(request):
    return render_to_response('pm/index.html')