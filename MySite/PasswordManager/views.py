from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from .models import Group, Account


class IndexView(generic.ListView):
    template_name = 'pm/index.html'
    context_object_name = "all_groups"

    def get_queryset(self):
        return Group.objects.all()


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