from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ChessDebriefer.Logic.accuracy import calculate_accuracy
from ChessDebriefer.Logic.compare import calculate_opening_comparisons, calculate_percentages_comparisons, \
    calculate_event_comparisons, calculate_termination_comparisons
from ChessDebriefer.Logic.openings import calculate_eco_stats
from ChessDebriefer.Logic.general import handle_pgn_uploads, handle_pgn_openings_upload
from ChessDebriefer.Logic.percentages_database import calculate_percentages_database, \
    calculate_event_percentages_database, calculate_termination_percentages_database, \
    calculate_opening_percentages_database


# TODO remove
def debug(request):
    return HttpResponse(status=200)


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        handle_pgn_uploads(request.FILES['file'])
        return HttpResponse("Success! Your file was uploaded and is now being parsed. Please note that it may take "
                            "several hours for the process to complete")
    else:
        return HttpResponse(status=405)


@csrf_exempt
def upload_openings(request):
    if request.method == 'POST':
        handle_pgn_openings_upload(request.FILES['file'])
        return HttpResponse("Success! Your file was uploaded and is now being parsed. Please note that it may take "
                            "several hours for the process to complete")
    else:
        return HttpResponse(status=405)


def percentages(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_percentages_database(name, request.GET))
        # return JsonResponse(calculate_percentages(name, request.GET))
    else:
        return HttpResponse(status=405)


def compare_percentages(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_percentages_comparisons(name, request.GET))
    else:
        return HttpResponse(status=405)


def event_percentages(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_event_percentages_database(name, request.GET))
        # return JsonResponse(calculate_event_percentages(name, request.GET))
    else:
        return HttpResponse(status=405)


def compare_events(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_event_comparisons(name, request.GET))
    else:
        return HttpResponse(status=405)


def opening_percentages(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_opening_percentages_database(name, request.GET))
        # return JsonResponse(calculate_opening_percentages(name, request.GET))
    else:
        return HttpResponse(status=405)


def compare_openings(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_opening_comparisons(name, request.GET))
    else:
        return HttpResponse(status=405)


def termination_percentages(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_termination_percentages_database(name, request.GET))
        # return JsonResponse(calculate_termination_percentages(name, request.GET))
    else:
        return HttpResponse(status=405)


def compare_terminations(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_termination_comparisons(name, request.GET))
    else:
        return HttpResponse(status=405)


def accuracy(request, name):
    if request.method == 'GET':
        return JsonResponse(calculate_accuracy(name))
    else:
        return HttpResponse(status=405)


def opening_stats(request, eco):
    if request.method == 'GET':
        return JsonResponse(calculate_eco_stats(eco, request.GET))
    else:
        return HttpResponse(status=405)
