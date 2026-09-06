import os,json,requests
from bs4 import BeautifulSoup
BOT_TOKEN=os.environ["BOT_TOKEN"]
CHAT_ID=os.environ["CHAT_ID"]
PALAVRAS=["ssd","monitor","teclado","mouse","headset","controle","xbox","ps5","playstation","rtx","ryzen","intel","notebook","iphone","galaxy","8bitdo","logitech","astro","aula","switch","microfone"]
html=requests.get("https://www.promobit.com.br/",headers={"User-Agent":"Mozilla/5.0"},timeout=20).text
soup=BeautifulSoup(html,"html.parser")
try: enviados=json.load(open("ofertas.json","r",encoding="utf-8"))
except: enviados=[]
for a in soup.select("a[href*='/oferta/']"):
 t=a.get_text(" ",strip=True);h=a.get("href","");l="https://www.promobit.com.br"+h if h.startswith("/") else h
 if not t or not any(p in t.lower() for p in PALAVRAS) or l in enviados: continue
 requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",data={"chat_id":CHAT_ID,"text":f"🔥 OFERTA DE TECNOLOGIA\n\n🛒 {t}\n\n🔗 {l}"})
 enviados.append(l);json.dump(enviados,open("ofertas.json","w",encoding="utf-8"));break
