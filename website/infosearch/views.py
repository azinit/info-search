from django.shortcuts import render
from .services import bool_search, get_pages


# Create your views here.
def index(request):
    query = request.GET.get("q", "")
    results = bool_search(query)
    pages = get_pages(results)

    context = {
        "query": query,
        "results": results,
        "pages": pages,
    }
    return render(request, 'infosearch/index/index.html', context)
