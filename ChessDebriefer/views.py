from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from mongoengine import Q

from ChessDebriefer.forms import UploadPGNForm
from ChessDebriefer.logic import handle_pgn_uploads
from ChessDebriefer.models import Games


def test(request):
    html = '<html><body>Hello World!</body></html>'
    # for game in Games.objects:
    #    print(game.name)
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
    won_games = 0
    lost_games = 0
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    for game in games:
        if game.white == name:
            if game.result == "1-0":
                won_games = won_games + 1
            else:
                lost_games = lost_games + 1
        else:
            if game.result == "0-1":
                won_games = won_games + 1
            else:
                lost_games = lost_games + 1
    percentage_won = (won_games / (won_games + lost_games)) * 100
    percentage_lost = (lost_games / (won_games + lost_games)) * 100
    return HttpResponse("games won: " + str(won_games) + "\ngames lost: " + str(lost_games) + "\npercentage won: " +
                        str(round(percentage_won, 2)) + "%\npercentage lost: " + str(round(percentage_lost, 2)) + "%",
                        content_type="text/plain")
