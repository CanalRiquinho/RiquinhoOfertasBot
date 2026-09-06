import os
import re
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.promobit.com.br/"

PALAVRAS = [
    "ssd","nvme","monitor","teclado","mouse","headset",
    "controle","xbox","ps5","playstation","rtx","rx",
    "ryzen","intel","notebook","iphone","galaxy",
    "8bitdo","logitech","astro","aula","switch",
    "nintendo","microfone","webcam","cadeira"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

try:
    with open("ofertas.json", "r", encoding="utf-8") as f:
        enviados = json.load(f)
except:
    enviados = []

html = requests.get(URL, headers=HEADERS, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

cards = soup.select("a[href*='/oferta/']")

for card in cards:

    titulo = card.get_text(" ", strip=True)
    href = card.get("href", "")

    if href.startswith("/"):
        link = "https://www.promobit.com.br" + href
    else:
        link = href

    if not titulo:
        continue

    if not any(p in titulo.lower() for p in PALAVRAS):
        continue

    if link in enviados:
        continue

    # -------------------------
    # Abre a página da oferta
    # -------------------------
    pagina = requests.get(link, headers=HEADERS, timeout=20).text
    oferta = BeautifulSoup(pagina, "html.parser")

    imagem = ""

    og = oferta.find("meta", property="og:image")
    if og:
        imagem = og.get("content", "")

    preco = "Preço indisponível"

    texto = oferta.get_text(" ", strip=True)

    achou = re.search(r"R\$\s?[\d\.,]+", texto)

    if achou:
        preco = achou.group(0)

    caption = f"""🔥 OFERTA DE TECNOLOGIA

🛒 {titulo}

💰 {preco}

⚡ Oferta encontrada automaticamente
"""

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🛒 Ver Oferta",
                    "url": link
                }
            ]
        ]
    }

    if imagem:

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "photo": imagem,
                "caption": caption,
                "reply_markup": json.dumps(keyboard)
            }
        )

    else:

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": caption,
                "reply_markup": json.dumps(keyboard)
            }
        )

    enviados.append(link)

    with open("ofertas.json", "w", encoding="utf-8") as f:
        json.dump(enviados, f)

    break
