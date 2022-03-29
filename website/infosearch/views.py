from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        "query": request.GET.get("q", "")
    }
    return render(request, 'infosearch/index/index.html', context)
