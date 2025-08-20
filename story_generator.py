import os, random, textwrap, datetime, zipfile
"Et quelque part, un futur possible apprend à sourire."

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
pdf.multi_cell(0, 7, f"— {BRAND}\nAcheter les packs : {CTA_LINK}")
pdf.output(str(out_path))


def main():
today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
out_dir = Path("output") / today
free_dir = Path("free") / today
out_dir.mkdir(parents=True, exist_ok=True)
free_dir.mkdir(parents=True, exist_ok=True)

captions_lines = []
generated = []

for i in range(1, STORIES_PER_RUN + 1):
title = generate_title()
story = generate_story(WORDS_PER_STORY)
fname = f"histoire_{i:02d}.pdf"
save_pdf(title, story, out_dir / fname)
# garder aussi un .txt
(out_dir / f"histoire_{i:02d}.txt").write_text(f"{title}\n\n{story}", encoding="utf-8")
generated.append((title, fname))

# freebies (quelques histoires gratuites)
for j, (title, fname) in enumerate(generated[:FREEBIES_PER_RUN], start=1):
# copier les versions TXT dans free/ pour SEO + lecture rapide
src_txt = out_dir / fname.replace('.pdf', '.txt')
dst_txt = free_dir / f"free_{j:02d}.txt"
dst_txt.write_text(src_txt.read_text(encoding="utf-8"), encoding="utf-8")

# pack zip du jour (tout le dossier output/YYYY-MM-DD)
pack_name = f"pack_{today}.zip"
with zipfile.ZipFile(out_dir.parent / pack_name, 'w', zipfile.ZIP_DEFLATED) as zf:
for p in out_dir.rglob('*'):
zf.write(p, p.relative_to(out_dir.parent))

# captions prêtes pour Instagram/TikTok
for title, _ in generated:
captions_lines.append(
f"{title}\n— écrit par IA —\n\nLire des extraits gratuits sur le dépôt.\nPacks et abonnements ici → {CTA_LINK}\n\n#histoires #ia #ecriture #lecture #scifi #fantasy #thriller #france #livres #auteur"
)

(Path("captions") / today).mkdir(parents=True, exist_ok=True)
(Path("captions") / today / "captions.txt").write_text("\n\n---\n\n".join(captions_lines), encoding="utf-8")

# index simple des freebies
index = Path("free/index.md")
existing = index.read_text(encoding="utf-8") if index.exists() else "# Extraits gratuits\n\n"
existing += f"\n## {today}\n"
for j in range(1, FREEBIES_PER_RUN + 1):
existing += f"- [{today}/free_{j:02d}.txt](./{today}/free_{j:02d}.txt)\n"
index.write_text(existing, encoding="utf-8")

if __name__ == "__main__":
main()
