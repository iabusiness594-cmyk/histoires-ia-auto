import os
import random
import textwrap
import datetime
import zipfile
from pathlib import Path
from fpdf import FPDF

# Constantes
BRAND = "Histoires IA"
CTA_LINK = "https://ton-site.com"

def generate_story():
    intro = "Et quelque part, un futur possible apprend à sourire."
    body = [
        "Un personnage découvre un nouveau monde rempli de mystères.",
        "Un choix difficile se présente, changeant le cours de son histoire.",
        "Une rencontre inattendue apporte espoir et courage."
    ]
    twist = "Mais rien ne se passe comme prévu..."
    outro = "Et c’est ainsi qu’une nouvelle aventure commence."

    return "\n\n".join([intro] + body + [twist, outro])


def save_pdf(title: str, text: str, out_path: Path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, title)
    pdf.ln(4)

    pdf.set_font("Helvetica", size=12)
    for para in text.split("\n\n"):
        wrapped = textwrap.fill(para, width=90)
        pdf.multi_cell(0, 7, wrapped)
        pdf.ln(2)

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 11)
    pdf.multi_cell(0, 7, f"-- {BRAND}\nAcheter les packs : {CTA_LINK}")

    pdf.output(str(out_path))


def main():
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = Path("output") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    story_text = generate_story()
    title = "Histoire générée"

    out_path = out_dir / f"{title.replace(' ', '_')}.pdf"
    save_pdf(title, story_text, out_path)

    # Optionnel : zip de sortie
    zip_path = f"{out_dir}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(out_path, out_path.name)

    print(f"Histoire générée : {out_path}")
    print(f"Archive créée : {zip_path}")


if __name__ == "__main__":
    main()
