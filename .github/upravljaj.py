"""Obrađuje issue s naslovom 'Dodaj: X' ili 'Ukloni: X' i ažurira subjekti.txt."""
import os
from pathlib import Path

naslov = os.environ.get("NASLOV", "").strip()
akcija, _, pojam = naslov.partition(":")
akcija, pojam = akcija.strip().lower(), " ".join(pojam.split())
datoteka = Path("subjekti.txt")
retci = datoteka.read_text(encoding="utf-8").splitlines() if datoteka.exists() else []
postojeci = [r.strip() for r in retci if r.strip() and not r.strip().startswith("#")]
komentari = [r for r in retci if r.strip().startswith("#")]

if not (2 <= len(pojam) <= 100):
    poruka = f"Neispravan pojam „{pojam}” – upišite OIB ili naziv (2–100 znakova)."
elif akcija == "dodaj":
    if pojam.lower() in (p.lower() for p in postojeci):
        poruka = f"„{pojam}” se već prati."
    else:
        postojeci.append(pojam)
        poruka = (f"Dodano praćenje: {pojam}. Prva provjera (s popisom postojećih objava) "
                  "stiže uz sljedeću večernju provjeru.")
elif akcija == "ukloni":
    novi = [p for p in postojeci if p.lower() != pojam.lower()]
    poruka = (f"Uklonjeno praćenje: {pojam}." if len(novi) < len(postojeci)
              else f"„{pojam}” nije bio na popisu.")
    postojeci = novi
else:
    poruka = "Nepoznata naredba – naslov mora počinjati s 'Dodaj:' ili 'Ukloni:'."

datoteka.write_text("\n".join(komentari + postojeci) + "\n", encoding="utf-8")
with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
    f.write(f"poruka={poruka}\n")
print(poruka)
