from django.shortcuts import render
from django.core.paginator import Paginator
import requests
import os

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


API_KEY = os.getenv("NEWS_API_KEY", "78f7169812b042e2a4d41f1065b4d6ed")
BASE_URL = "https://newsapi.org/v2/top-headlines"


def filtragem(request):
    categoria = request.GET.get("categoria", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")
    pesquisa = request.GET.get("pesquisa", "")

    endpoint = (
        "https://newsapi.org/v2/everything"
        if pesquisa
        else "https://newsapi.org/v2/top-headlines"
    )

    params = {
        "apiKey": API_KEY,
        "language": "pt",
        "pageSize": 50,
    }

    if pesquisa:
        
        params["qInTitle"] = pesquisa 
        params["sortBy"] = "relevancy"
        params["searchIn"] = "title,description,content"  # campos usados
        
        params["excludeDomains"] = "youtube.com,facebook.com,globo.com"
    else:
        params["country"] = "br"
        if categoria:
            params["category"] = categoria

    
    if data_inicio:
        params["from"] = data_inicio
    if data_fim:
        params["to"] = data_fim

    
    response = requests.get(endpoint, params=params)
    data_json = response.json()
    articles = data_json.get("articles", []) if data_json.get("status") == "ok" else []

   
    paginator = Paginator(articles, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categoria": categoria,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "pesquisa": pesquisa,
        "total_noticias": paginator.count,
    }
    return render(request, "homepage/filtragem.html", context)
