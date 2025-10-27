from django.shortcuts import render
from django.core.paginator import Paginator
import requests
import os

API_KEY = os.getenv("NEWS_API_KEY", "78f7169812b042e2a4d41f1065b4d6ed")
BASE_URL = "https://newsapi.org/v2/top-headlines"


def index(request):
    return render(request, "homepage/index.html")


def contato(request):
    """Página de contato simples."""
    return render(request, "homepage/contato.html")


def faq(request):
    """Página de perguntas frequentes."""
    return render(request, "homepage/faq.html")


def sobrenos(request):
    """Página sobre nós."""
    return render(request, "homepage/sobrenos.html")


def filtragem(request):
    """Filtra notícias pela API externa com paginação e busca."""
    categoria = request.GET.get("categoria", "")
    data = request.GET.get("data", "")
    pesquisa = request.GET.get("pesquisa", "")

    endpoint = (
        "https://newsapi.org/v2/top-headlines"
        if not pesquisa
        else "https://newsapi.org/v2/everything"
    )

    params = {
        "apiKey": API_KEY,
        "pageSize": 50,
        "language": "pt",
    }

    if pesquisa:
        params["q"] = pesquisa
        params["sortBy"] = "publishedAt"
    else:
        params["country"] = "br"
        if categoria:
            params["category"] = categoria

    if data:
        params["from"] = data

    response = requests.get(endpoint, params=params)
    data_json = response.json()

    # Se der erro na API, evita travar o site
    articles = data_json.get("articles", []) if data_json.get("status") == "ok" else []

    paginator = Paginator(articles, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categoria": categoria,
        "data_noticia": data,
        "pesquisa": pesquisa,
        "total_noticias": paginator.count,
    }
    return render(request, "homepage/filtragem.html", context)
