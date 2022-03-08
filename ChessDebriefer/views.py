from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from ChessDebriefer.forms import UploadPGNForm
from ChessDebriefer.logic import handle_pgn_uploads, calculate_accuracy, calculate_percentages


def test(request):
    html = '<html><body>Hello World!</body></html>'
    params = request.GET
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
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)


def success(request):
    return HttpResponse("Success!")


def percentages(request, name):
    stats = calculate_percentages(name, request.GET)
    return JsonResponse(stats)


def accuracy(request, name):
    percentage = calculate_accuracy(name)
    return HttpResponse(str(percentage) + " %")
