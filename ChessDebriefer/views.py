from django.http import HttpResponse


def test(request):
    html = '<html><body>Hello World!</body></html>'
    return HttpResponse("Hello World!")  # html
