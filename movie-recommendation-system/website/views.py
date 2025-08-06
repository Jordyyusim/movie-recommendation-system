from django.shortcuts import render
from .utils.main import recommend

rec = recommend()

def index(request):
    toppicks = rec.top_picks()
    return render (request, 'index.html', context={"top":toppicks})

def result(request):
    filmya = request.GET.get('film', '').lower()
    hasilrek, informasi = rec.main(filmya)
    if hasilrek == []:
        return render (request, 'error.html', context={"eror":"MOVIE DOESNT EXIST"})
    else:
        return render (request, 'result.html', context={"rek":hasilrek, "detail":informasi})