"""Gera loja.html a partir de copy/05-loja.md mantendo estilo minimalista.

Regras:
- Cabecalho/nav identicos as outras paginas
- TOC no topo com links para 23 categorias (anchors cat-1..cat-23)
- Cada categoria: h2 com id="cat-N"
- Cada produto: h3 (com id slug) + paragrafos (Beneficio, Como funciona, Para quem, Duracao, Preco, CTA)
- Subcategorias dentro de uma categoria viram h3-pai usando blockquote/strong
- Tabelas markdown viram tabelas HTML
- Blockquotes do md viram <p class="note">
- Substitui caracteres especiais para versao ascii leve, mantendo acentos PT-PT
- "Voltar ao topo" no final de cada categoria
"""
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "copy" / "05-loja.md"
DST = ROOT / "preview" / "loja.html"

text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()

def esc(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))

def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s

# Inline formatting: **bold** -> <strong>, [text](url) -> <a>
def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s

NAV = """<nav>
  <a href="index.html">Home</a>
  <a href="sobre.html">Sobre</a>
  <a href="metodo.html">Metodo</a>
  <a href="tratamentos.html">Tratamentos</a>
  <a href="loja.html">Loja</a>
  <a href="resultados.html">Resultados</a>
  <a href="contacto.html">Contacto</a>
  <a href="politicas.html">Politicas</a>
</nav>"""

out = []
out.append('<!doctype html>')
out.append('<html lang="pt-PT">')
out.append('<head>')
out.append('<meta charset="utf-8">')
out.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
out.append('<title>Loja Online | Clinica Aromas do Deserto</title>')
out.append('<link rel="stylesheet" href="assets/style.css">')
out.append('</head>')
out.append('<body id="topo">')
out.append('')
out.append(NAV)
out.append('')
out.append('<span class="tag">Pagina: Loja Online — PT-PT — 23 categorias, 297 produtos</span>')
out.append('')

# State
i = 0
n = len(lines)
in_table = False
table_buffer = []
current_cat = None  # number (int) of categoria aberta
toc_entries = []  # list of (anchor, title)
body_chunks = []

# First pass: collect toc
cat_re = re.compile(r"^### Categoria (\d+) — (.+)$")
for ln in lines:
    m = cat_re.match(ln)
    if m:
        num = int(m.group(1))
        title = m.group(2).strip()
        toc_entries.append((f"cat-{num}", num, title))

# Now do conversion. We'll do a stateful walk.
buf = []  # list of html lines to emit (for body)

def flush_table():
    global table_buffer
    if not table_buffer:
        return
    rows = table_buffer
    table_buffer = []
    # rows: list of list of cell strings
    if not rows:
        return
    html = ['<table>']
    # header
    header = rows[0]
    html.append('  <tr>' + ''.join(f'<th>{inline(c.strip())}</th>' for c in header) + '</tr>')
    for r in rows[2:] if len(rows) > 1 else []:  # skip separator row at idx 1
        html.append('  <tr>' + ''.join(f'<td>{inline(c.strip())}</td>' for c in r) + '</tr>')
    html.append('</table>')
    buf.append('\n'.join(html))

def open_categoria(num, title):
    anchor = f"cat-{num}"
    buf.append(f'<h2 id="{anchor}">Categoria {num} — {esc(title)}</h2>')

# We treat the file in sections:
# - Skip everything before "## Hero"
# - Hero -> custom hero block
# - Seccao 1 / Seccao 2 (intro) -> normal
# - "## Catalogo Completo" marker
# - "### Categoria N — X" -> h2
# - "#### Name" -> h3 (product) - id slug
# - "##### Name" -> h4 (sub-product within categoria) - some categorias use 4-level
# - blockquote (>)  -> <p class="note">
# - tables -> table
# - other -> paragraphs / strong

# We'll find sections of interest

# Build TOC HTML
toc_html = ['<h2 id="categorias">Categorias</h2>']
toc_html.append('<ol>')
for anchor, num, title in toc_entries:
    toc_html.append(f'  <li><a href="#{anchor}">{esc(title)}</a></li>')
toc_html.append('</ol>')

# Walk lines — skip everything until first "## Hero"
i = 0
while i < n and not lines[i].strip().startswith('## Hero'):
    i += 1
emitted_hero = False
emitted_intro = False

while i < n:
    line = lines[i]
    stripped = line.rstrip()

    # Detect tables (markdown pipe tables)
    if stripped.startswith('|') and '|' in stripped[1:]:
        # collect contiguous table rows
        rows = []
        while i < n and lines[i].strip().startswith('|'):
            row = [c for c in lines[i].strip().strip('|').split('|')]
            rows.append(row)
            i += 1
        # render
        if len(rows) >= 2:
            html = ['<table>']
            header = rows[0]
            html.append('  <tr>' + ''.join(f'<th>{inline(c.strip())}</th>' for c in header) + '</tr>')
            data_rows = rows[2:] if all(set(c.strip()) <= set('-: ') for c in rows[1]) else rows[1:]
            for r in data_rows:
                # pad
                while len(r) < len(header):
                    r.append('')
                html.append('  <tr>' + ''.join(f'<td>{inline(c.strip())}</td>' for c in r) + '</tr>')
            html.append('</table>')
            buf.append('\n'.join(html))
        continue

    # Categoria header
    m = cat_re.match(stripped)
    if m:
        num = int(m.group(1))
        title = m.group(2).strip()
        # If transitioning between categories, add 'voltar ao topo'
        if current_cat is not None:
            buf.append('<p class="note"><a href="#topo">Voltar ao topo</a> · <a href="#categorias">Ver todas as categorias</a></p>')
        current_cat = num
        anchor = f"cat-{num}"
        buf.append(f'<h2 id="{anchor}">Categoria {num} — {esc(title)}</h2>')
        i += 1
        continue

    # Sub-categoria title within categoria (#### Foo or ##### Foo)
    if stripped.startswith('#### '):
        title = stripped[5:].strip()
        sid = slugify(title)
        buf.append(f'<h3 id="{sid}">{esc(title)}</h3>')
        i += 1
        continue
    if stripped.startswith('##### '):
        title = stripped[6:].strip()
        sid = slugify(title)
        buf.append(f'<h4 id="{sid}">{esc(title)}</h4>')
        i += 1
        continue
    if stripped.startswith('### '):
        # Generic ### (used inside categoria for subgroups like "Mulher — Sessao Avulsa")
        title = stripped[4:].strip()
        # If matches "Categoria N", handled above; otherwise treat as h3
        sid = slugify(title)
        buf.append(f'<h3 id="{sid}">{esc(title)}</h3>')
        i += 1
        continue

    # Top-level ## (sections like Hero, Seccao 1, Catalogo, Seccao Final, SEO)
    if stripped.startswith('## '):
        title = stripped[3:].strip()
        # Skip SEO section entirely (footer covers it). Stop rendering at SEO.
        if title == 'SEO':
            break
        # Skip rendering "Catalogo Completo" wrapper (we do TOC there)
        if title in ('Catalogo Completo', 'Catálogo Completo'):
            buf.append('')
            buf.extend(toc_html)
            buf.append('')
            i += 1
            continue
        if title.startswith('Hero'):
            # render hero block
            i += 1
            # skip blank lines after "## Hero"
            while i < n and not lines[i].strip():
                i += 1
            # parse following bullet lines (stop at next ## or ---)
            hero = {}
            while i < n and not lines[i].lstrip().startswith('##') and lines[i].strip() != '---':
                ln = lines[i].strip()
                if ln.startswith('- **Headline:**'):
                    hero['headline'] = ln.split(':**', 1)[1].strip()
                elif ln.startswith('- **Subheadline:**'):
                    hero['sub'] = ln.split(':**', 1)[1].strip()
                elif ln.startswith('- **CTA principal:**'):
                    hero['cta1'] = ln.split(':**', 1)[1].strip()
                elif ln.startswith('- **CTA secundário:**') or ln.startswith('- **CTA secundario:**'):
                    hero['cta2'] = ln.split(':**', 1)[1].strip()
                i += 1
            buf.append(f"<h1>{esc(hero.get('headline',''))}</h1>")
            if hero.get('sub'):
                buf.append(f"<p>{esc(hero['sub'])}</p>")
            cta = []
            if hero.get('cta1'):
                cta.append(f'<a href="contacto.html">{esc(hero["cta1"])}</a>')
            if hero.get('cta2'):
                cta.append(f'<a href="#cat-17">{esc(hero["cta2"])}</a>')
            if cta:
                buf.append('<div class="cta">' + ' '.join(cta) + '</div>')
            continue
        # Skip "Secção 2 — Filtros e categorias" (just a hint, render briefly)
        sid = slugify(title)
        buf.append(f'<h2 id="{sid}">{esc(title)}</h2>')
        i += 1
        continue

    # blockquote
    if stripped.startswith('>'):
        # collect contiguous quote lines
        block = []
        while i < n and lines[i].lstrip().startswith('>'):
            block.append(lines[i].lstrip()[1:].lstrip())
            i += 1
        joined = ' '.join(b for b in block if b)
        if joined:
            buf.append(f'<p class="note">{inline(joined)}</p>')
        continue

    # bullet list
    if stripped.startswith('- '):
        items = []
        while i < n and lines[i].strip().startswith('- '):
            items.append(lines[i].strip()[2:])
            i += 1
        buf.append('<ul>')
        for it in items:
            buf.append(f'  <li>{inline(it)}</li>')
        buf.append('</ul>')
        continue

    # numbered list
    if re.match(r'^\d+\.\s', stripped):
        items = []
        while i < n and re.match(r'^\d+\.\s', lines[i].strip()):
            items.append(re.sub(r'^\d+\.\s', '', lines[i].strip()))
            i += 1
        buf.append('<ol>')
        for it in items:
            buf.append(f'  <li>{inline(it)}</li>')
        buf.append('</ol>')
        continue

    # horizontal rule
    if stripped == '---':
        i += 1
        continue

    # blank
    if not stripped:
        i += 1
        continue

    # Skip the YAML-ish front block at top (before first H1)
    if stripped.startswith('# '):
        i += 1
        continue

    # Plain paragraph
    # Collect contiguous paragraph lines
    para = [stripped]
    i += 1
    while i < n and lines[i].strip() and not lines[i].lstrip().startswith(('#', '-', '>', '|')) and not re.match(r'^\d+\.\s', lines[i].strip()) and lines[i].strip() != '---':
        para.append(lines[i].rstrip())
        i += 1
    joined = ' '.join(para).strip()
    if joined:
        buf.append(f'<p>{inline(joined)}</p>')

# Final voltar ao topo
if current_cat is not None:
    buf.append('<p class="note"><a href="#topo">Voltar ao topo</a> · <a href="#categorias">Ver todas as categorias</a></p>')

# Footer
buf.append('')
buf.append('<footer>')
buf.append('SEO — Meta title: Loja Online | Tratamentos, Vouchers e SPA — Aromas do Deserto<br>')
buf.append('Meta description: Reserve protocolos, vouchers SPA, packs de massagem e cartoes presente da Clinica Aromas do Deserto, Braga.<br>')
buf.append('Slug: /loja')
buf.append('</footer>')
buf.append('')
buf.append('</body>')
buf.append('</html>')

out.extend(buf)

DST.write_text('\n'.join(out), encoding='utf-8')
print(f"OK: {DST} ({sum(1 for _ in open(DST, encoding='utf-8'))} linhas)")
