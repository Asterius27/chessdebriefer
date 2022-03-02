from django.http import HttpResponse

from ChessDebriefer.models import Games


def test(request):
    html = '<html><body>Hello World!</body></html>'
    Games(name='prova').save()
    for name in Games.objects:
        print(name.name)
    return HttpResponse("Hello World!")  # html
