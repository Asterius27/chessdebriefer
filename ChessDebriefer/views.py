from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ChessDebriefer.forms import UploadPGNForm
from ChessDebriefer.logic import handle_pgn_uploads, evaluate_games, calculate_percentages


def test(request):
    html = '<html><body>Hello World!</body></html>'
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
    (percentage_won, percentage_lost, percentage_drawn, won_games, lost_games, drawn_games) = calculate_percentages(name)
    return HttpResponse("games won: " + str(won_games) + "\ngames lost: " + str(lost_games) +
                        "\ngames drawn: " + str(drawn_games) + "\npercentage won: " + str(round(percentage_won, 2)) +
                        " %\npercentage lost: " + str(round(percentage_lost, 2)) + " %\npercentage drawn: " +
                        str(round(percentage_drawn, 2)) + " %", content_type="text/plain")


def accuracy(request, name):
    percentage = evaluate_games(name)
    return HttpResponse(str(round(percentage, 2)) + " %")
