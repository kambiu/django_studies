from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Album

""" generic view """


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = "all_albums"

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    # for pass in , refer to the urls.py
    model = Album # this only work for url pass in parameters
    template_name = 'music/detail.html'

    # create by myself, for pass other details
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['now'] = "111"
        return context


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'album_logo']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy("music:index")