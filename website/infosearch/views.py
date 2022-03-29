from django.shortcuts import render
from .services import bool_search


# Create your views here.
def index(request):
    query = request.GET.get("q", "")
    results = bool_search(query)

    context = {
        "query": query,
        "results": results,
    }
    return render(request, 'infosearch/index/index.html', context)
