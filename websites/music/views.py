from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Album
from django.http import Http404
# Create your views here.

def index(request):

    all_album = Album.objects.all()
    # choose default directory /templates/ <- not need to specify
    # template = loader.get_template('music/index.html')
    context = {
        'all_album': all_album,
    }
    return render(request, 'music/index.html', context)

    # pass a dict to the html page
    return HttpResponse(template.render(context, request))


def detail(request, album_id):
    # return HttpResponse("<h2>Details for Album ID:" + str(album_id) + " </h2>")
    # try:
    #     album = Album.objects.get(pk=album_id)
    # except Album.DoesNotExist:
    #     raise Http404("Album does not exist")
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})