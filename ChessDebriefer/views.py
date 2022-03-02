from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ChessDebriefer.forms import UploadPGNForm
from ChessDebriefer.logic import handle_pgn_uploads
from ChessDebriefer.models import Games


def test(request):
    html = '<html><body>Hello World!</body></html>'
    # Games(name='prova').save()
    # for name in Games.objects:
    #    print(name.name)
    return HttpResponse("Hello World!")  # html


def upload(request):
    if request.method == 'GET':
        form = UploadPGNForm()
        return render(request, 'uploadpgn.html', {'form': form})
    if request.method == 'POST':
        form = UploadPGNForm(request.POST, request.FILES)
        if form.is_valid():
            handle_pgn_uploads(request.FILES['file'])
            return HttpResponseRedirect('/success')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponse(status=400)


def success(request):
    return HttpResponse("Success!")
