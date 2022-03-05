from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ChessDebriefer.forms import UploadPGNForm
from ChessDebriefer.logic import handle_pgn_uploads, evaluate_games, calculate_percentages


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
    return HttpResponse("games won: " + str(stats[0]) + "\ngames lost: " + str(stats[1]) +
                        "\ngames drawn: " + str(stats[2]) + "\npercentage won: " + str(round(stats[3], 2)) +
                        " %\npercentage lost: " + str(round(stats[4], 2)) + " %\npercentage drawn: " +
                        str(round(stats[5], 2)) + " %", content_type="text/plain")


def accuracy(request, name):
    percentage = evaluate_games(name)
    return HttpResponse(str(round(percentage, 2)) + " %")
