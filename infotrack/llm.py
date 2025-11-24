# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from newsapi import NewsApiClient
from ollama import Client

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY

# -------------------------
# Configurações
# -------------------------

newsapi = NewsApiClient(api_key='')

hoje = datetime.utcnow()
uma_semana_atras = hoje - timedelta(days=7)
from_date = uma_semana_atras.strftime("%Y-%m-%d")
to_date = hoje.strftime("%Y-%m-%d")

# -------------------------
# Busca as notícias
# -------------------------

res = newsapi.get_everything(
    q="ai",
    from_param=from_date,
    sources='bbc-news,the-verge',
    domains='bbc.co.uk,techcrunch.com',
    to=to_date,
    language='en',
    sort_by="publishedAt",
    page_size=3,
    page=1
)

artigos = res.get("articles", [])

if not artigos:
    print("nenhuma noticia encontrada essa semana.")
    exit()

# -------------------------
# Resumir cada artigo individualmente via Ollama
# -------------------------

client = Client()
resumos_individuais = []

for art in artigos:
    titulo = art.get("title", "")
    descricao = art.get("description", "") or ""
    conteudo = art.get("content", "") or ""

    texto_artigo = f"{titulo}\n{descricao}\n{conteudo}"

    prompt = f"Resuma de forma jornalística, rápida e objetiva a notícia abaixo:\n\n{texto_artigo}"

    # chama o ollama para CADA artigo
    resposta = client.chat(
        model="gemma3:4b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    resumo = resposta["message"]["content"]
    resumos_individuais.append(resumo)

# monta o texto final juntando todos os resumos
resumo_semana = "\n\n****************************************\n\n".join(resumos_individuais)

print("Resumo gerado com sucesso.\n")

# -------------------------
# Gerar PDF
# -------------------------

pdf_nome = "resumo_semanal_newsapi.pdf"

doc = SimpleDocTemplate(
    pdf_nome,
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=20 * mm
)

styles = getSampleStyleSheet()
title_style = styles["Title"]
title_style.alignment = 1
title_style.spaceAfter = 12

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=14,
    alignment=TA_JUSTIFY
)

elements = []
elements.append(Paragraph("Resumo semanal de notícias", title_style))
elements.append(Spacer(1, 8))

paragrafos = resumo_semana.split("\n\n")

for p in paragrafos:
    p = p.strip()
    if p:
        elements.append(Paragraph(p.replace("\n", "<br/>"), body_style))
        elements.append(Spacer(1, 6))

doc.build(elements)

print(f"PDF gerado: {pdf_nome}")

