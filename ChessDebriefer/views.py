from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from ChessDebriefer.Logic.accuracy import calculate_accuracy
from ChessDebriefer.Logic.openings import calculate_eco_stats
from ChessDebriefer.Logic.percentages import calculate_percentages, calculate_event_percentages, \
    calculate_opening_percentages, calculate_termination_percentages
from ChessDebriefer.forms import UploadPGNForm
from ChessDebriefer.Logic.general import handle_pgn_uploads, handle_pgn_openings_upload


def test(request):
    return HttpResponse("Hello World!")


def success(request):
    return HttpResponse("Success! Your file was uploaded and is now being parsed. Please note that it may take several "
                        "hours for the process to complete")


def upload(request):
    if request.method == 'GET':
        form = UploadPGNForm()
        return render(request, 'upload_pgn.html', {'form': form})
    if request.method == 'POST':
        form = UploadPGNForm(request.POST, request.FILES)
        if form.is_valid():
            handle_pgn_uploads(request.FILES['file'])
            return HttpResponseRedirect('/success')
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)


def upload_openings(request):
    if request.method == 'GET':
        form = UploadPGNForm()
        return render(request, 'upload_pgn_openings.html', {'form': form})
    if request.method == 'POST':
        form = UploadPGNForm(request.POST, request.FILES)
        if form.is_valid():
            handle_pgn_openings_upload(request.FILES['file'])
            return HttpResponseRedirect('/success')
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)


def percentages(request, name):
    return JsonResponse(calculate_percentages(name, request.GET))


def event_percentages(request, name):
    return JsonResponse(calculate_event_percentages(name, request.GET))


def opening_percentages(request, name):
    return JsonResponse(calculate_opening_percentages(name, request.GET))


def termination_percentages(request, name):
    return JsonResponse(calculate_termination_percentages(name, request.GET))


def accuracy(request, name):
    return JsonResponse({"accuracy_percentage": calculate_accuracy(name)})


def opening_stats(request, eco):
    return JsonResponse(calculate_eco_stats(eco, request.GET))
