"""Gera loja.html a partir de copy/05-loja.md.

Estrutura v2 (2026-05-06):
- ## Hero -> hero block
- ## Seccao 1 / 2 -> intro
- # Catalogo -> ignorar (so marcador), inserir TOC depois
- ## Categoria N — Nome -> h2#cat-N
- ### Produto                       -> <article class="product">
  Bloco do produto:
  - **Campo:** valor   -> <p><strong>Campo:</strong> valor</p>
  - tabela variacoes   -> <table class="variations">
  - linha curta tipo: **€90 — 60 min** | CTA: Marcar consulta
                       -> <p class="price-line">...
  - **CTA:** ...       -> <p class="cta-line">CTA: ...</p>
- ### Subcategoria 16.1 — Nome -> <h3 class="subcategoria">
- **Pack X** (em paragrafo, sem heading) dentro de subcategoria  -> <article class="product">
- > blockquote -> <p class="note">

Visual mantido: hero, cards .product, paleta terracota, container 800px.
"""
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "copy" / "05-loja.md"
DST = ROOT / "preview" / "loja.html"

text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()
n = len(lines)

def esc(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))

def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s

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
  <a href="loja.html" class="active">Loja</a>
  <a href="resultados.html">Resultados</a>
  <a href="contacto.html">Contacto</a>
  <a href="politicas.html">Politicas</a>
</nav>"""

# ---- First pass: contar produtos por categoria e coletar TOC
cat_re = re.compile(r"^## Categoria (\d+) — (.+)$")
prod_re = re.compile(r"^### (?!Subcategoria )(?!Categoria )(.+)$")
sub_re = re.compile(r"^### Subcategoria (\d+)\.(\d+) — (.+)$")
# "Pack" como produto sem heading: linha que comeca com **Nome** em negrito (tipo "**Pack Mini Spa Party**")
pack_inline_re = re.compile(r"^\*\*([^*]+)\*\*\s*$")

categorias = []  # list of dict {num, title, count}
current_cat_idx = -1

i = 0
while i < n:
    ln = lines[i].rstrip()
    m = cat_re.match(ln)
    if m:
        categorias.append({"num": int(m.group(1)), "title": m.group(2).strip(), "count": 0})
        current_cat_idx = len(categorias) - 1
        i += 1
        continue
    if current_cat_idx >= 0:
        if prod_re.match(ln) and not sub_re.match(ln):
            categorias[current_cat_idx]["count"] += 1
        else:
            mp = pack_inline_re.match(ln)
            if mp and ':' not in mp.group(1):
                # pack-inline: linha "**Nome**" sozinha sem ":"
                categorias[current_cat_idx]["count"] += 1
    i += 1

total_produtos = sum(c["count"] for c in categorias)

# ---- Second pass: gerar HTML
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
out.append('<div class="page">')
out.append('')
out.append('<div class="hero">')
out.append(f'<span class="tag">Pagina: Loja Online — PT-PT — 23 categorias, {total_produtos} produtos-pai</span>')
# Hero parsed below

buf = []  # body chunks (apos hero)
hero_lines = []  # lines do hero
in_hero = False
hero_done = False
seccao1_done = False

# We'll build a state machine
i = 0

def parse_table(start_idx):
    """Parse markdown pipe table starting at start_idx. Return (rows, next_idx)."""
    rows = []
    j = start_idx
    while j < n and lines[j].strip().startswith('|'):
        row = [c.strip() for c in lines[j].strip().strip('|').split('|')]
        rows.append(row)
        j += 1
    return rows, j

def render_variations_table(rows, classname="variations"):
    """Renderiza tabela de variacoes. Detecta separator row e ignora.
    Coluna preco (ultima) recebe class='price'."""
    if len(rows) < 2:
        return ''
    header = rows[0]
    # Detect separator row (---|---)
    if all(set(c) <= set('-: ') for c in rows[1]):
        data = rows[2:]
    else:
        data = rows[1:]
    # Detect price column (last col que comeca com € ou contem €)
    price_col_idx = len(header) - 1
    # Heuristica: ultima coluna = preco (sempre, nessas tabelas)
    html = [f'<table class="{classname}">']
    html.append('  <thead><tr>' + ''.join(
        f'<th{" class=\"price-col\"" if k == price_col_idx else ""}>{inline(c)}</th>'
        for k, c in enumerate(header)) + '</tr></thead>')
    html.append('  <tbody>')
    for r in data:
        while len(r) < len(header):
            r.append('')
        cells = []
        for k, c in enumerate(r):
            if k == price_col_idx:
                cells.append(f'<td class="price-col">{inline(c)}</td>')
            else:
                cells.append(f'<td>{inline(c)}</td>')
        html.append('  <tr>' + ''.join(cells) + '</tr>')
    html.append('  </tbody>')
    html.append('</table>')
    return '\n'.join(html)

# Helpers
def emit_hero(headline, sub, cta1, cta2):
    out.append(f'<h1>{esc(headline)}</h1>')
    if sub:
        out.append(f'<p class="lead">{esc(sub)}</p>')
    cta = []
    if cta1:
        cta.append(f'<a href="contacto.html">{esc(cta1)}</a>')
    if cta2:
        cta.append(f'<a href="#cat-17">{esc(cta2)}</a>')
    if cta:
        out.append('<div class="cta">' + ' '.join(cta) + '</div>')
    out.append('</div>')  # close hero

# ---- Walk
# Skip until "## Hero"
while i < n and not lines[i].strip().startswith('## Hero'):
    i += 1

# Parse Hero
i += 1  # skip "## Hero"
hero = {}
while i < n:
    ln = lines[i].strip()
    if ln.startswith('## ') or ln == '---':
        break
    if ln.startswith('- **Headline:**'):
        hero['h'] = ln.split(':**', 1)[1].strip()
    elif ln.startswith('- **Subheadline:**'):
        hero['s'] = ln.split(':**', 1)[1].strip()
    elif ln.startswith('- **CTA principal:**'):
        hero['c1'] = ln.split(':**', 1)[1].strip()
    elif ln.startswith('- **CTA secundario:**') or ln.startswith('- **CTA secundário:**'):
        hero['c2'] = ln.split(':**', 1)[1].strip()
    i += 1

emit_hero(hero.get('h',''), hero.get('s',''), hero.get('c1',''), hero.get('c2',''))

# Build TOC HTML (will be injected after intro)
toc_lines = ['<h2 id="categorias">Categorias</h2>', '<ol>']
for c in categorias:
    toc_lines.append(f'  <li><a href="#cat-{c["num"]}">{esc(c["title"])} <span class="cat-count">({c["count"]})</span></a></li>')
toc_lines.append('</ol>')

# Continue walk: render Seccao 1, then TOC, then Catalogo
current_cat = None  # int

def is_field_line(ln):
    """Linha tipo **Campo:** valor"""
    return bool(re.match(r'^\*\*[^*]+:\*\*\s', ln))

def is_short_price_line(ln):
    """Linha curta: **€90 — 60 min** | CTA: Marcar consulta
    ou: **Sob consulta** | CTA: ..."""
    return bool(re.match(r'^\*\*[€a-zA-Z0-9].*\*\*\s*\|\s*CTA:', ln))

def split_short_price(ln):
    """Split em (price_md, cta_text)."""
    m = re.match(r'^(\*\*[^*]+\*\*)\s*\|\s*CTA:\s*(.+?)\s*$', ln)
    if m:
        return m.group(1), m.group(2)
    return None, None

def render_product_block(name, lines_block, is_pack=False):
    """Recebe nome do produto e lista de linhas do bloco. Renderiza article."""
    sid = slugify(name)
    html = [f'<article class="product">']
    html.append(f'<h3 id="{sid}">{esc(name)}</h3>')
    j = 0
    nb = len(lines_block)
    while j < nb:
        ln = lines_block[j].rstrip()
        s = ln.strip()
        if not s:
            j += 1
            continue
        # Tabela
        if s.startswith('|'):
            rows = []
            while j < nb and lines_block[j].strip().startswith('|'):
                row = [c.strip() for c in lines_block[j].strip().strip('|').split('|')]
                rows.append(row)
                j += 1
            html.append(render_variations_table(rows))
            continue
        # Variacoes header line: "**Variacoes:**" (label antes da tabela) - render como p compacto
        if s == '**Variacoes:**' or s == '**Variações:**':
            html.append('<p class="variations-label"><strong>Variações:</strong></p>')
            j += 1
            continue
        # Zona/Pack header before table: "**Beneficio principal:** ..." segue normal
        # Linha curta de preco: **€X — Ymin** | CTA: ...
        if is_short_price_line(s):
            price_md, cta_text = split_short_price(s)
            price_html = inline(price_md)  # vira <strong>...</strong>
            # transformar <strong> em <span class="price-tag">
            price_html = re.sub(r'<strong>(.+?)</strong>', r'<span class="price-tag">\1</span>', price_html, count=1)
            html.append(f'<p class="price-line">{price_html} <span class="cta-sep">·</span> <span class="cta-text">CTA: {esc(cta_text)}</span></p>')
            j += 1
            continue
        # **CTA:** ... linha sozinha
        m_cta = re.match(r'^\*\*CTA:\*\*\s*(.+?)\s*$', s)
        if m_cta:
            html.append(f'<p class="cta-line"><strong>CTA:</strong> {esc(m_cta.group(1))}</p>')
            j += 1
            continue
        # Campo: valor
        if is_field_line(s):
            # juntar paragrafo com linhas seguintes que nao sejam tabela/field/cta
            para = [s]
            j += 1
            while j < nb:
                nxt = lines_block[j].rstrip()
                ns = nxt.strip()
                if not ns:
                    break
                if ns.startswith('|') or is_field_line(ns) or is_short_price_line(ns) or ns.startswith('**CTA:**'):
                    break
                para.append(nxt)
                j += 1
            joined = ' '.join(para).strip()
            html.append(f'<p>{inline(joined)}</p>')
            continue
        # Paragrafo livre (descricao curta sem campos)
        para = [s]
        j += 1
        while j < nb:
            nxt = lines_block[j].rstrip()
            ns = nxt.strip()
            if not ns:
                break
            if ns.startswith('|') or is_field_line(ns) or is_short_price_line(ns) or ns.startswith('**CTA:**'):
                break
            para.append(nxt)
            j += 1
        joined = ' '.join(para).strip()
        html.append(f'<p>{inline(joined)}</p>')
    html.append('</article>')
    return '\n'.join(html)

def collect_product_block(start_idx):
    """A partir de uma linha apos ### Produto (ou apos **Pack X**), coleta linhas
    ate proximo ###, ## , #, ou separador ---. Retorna (block_lines, next_idx)."""
    block = []
    j = start_idx
    while j < n:
        ln = lines[j].rstrip()
        s = ln.strip()
        # Stop conditions
        if s.startswith('### ') or s.startswith('## ') or s.startswith('# '):
            break
        if s == '---':
            break
        # Outro pack inline (apos ja ter coletado conteudo, so se ja temos algum)
        if pack_inline_re.match(s) and len(block) > 0 and any(b.strip() for b in block):
            # check: e mesmo um pack? (texto curto e maiusculo no inicio)
            # heuristica: linha eh sozinha e nao e um campo (**X:**)
            # Se nao tem ":" no negrito, e um nome de produto-pack
            inner = pack_inline_re.match(s).group(1)
            if ':' not in inner:
                break
        block.append(ln)
        j += 1
    return block, j

# Main walk
hero_done = True
seccao_1_emitted = False
toc_emitted = False
out_body = []  # body content after hero

def emit(s):
    out_body.append(s)

while i < n:
    ln = lines[i].rstrip()
    s = ln.strip()

    # Top-level catalog marker
    if s == '# Catalogo' or s == '# Catálogo':
        # Inject TOC
        if not toc_emitted:
            emit('')
            for tl in toc_lines:
                emit(tl)
            emit('')
            toc_emitted = True
        i += 1
        continue

    # Categoria
    m_cat = cat_re.match(s)
    if m_cat:
        if current_cat is not None:
            emit('<p class="note"><a href="#topo">Voltar ao topo</a> · <a href="#categorias">Ver todas as categorias</a></p>')
        num = int(m_cat.group(1))
        title = m_cat.group(2).strip()
        current_cat = num
        emit(f'<h2 id="cat-{num}">Categoria {num} — {esc(title)}</h2>')
        i += 1
        continue

    # Subcategoria
    m_sub = sub_re.match(s)
    if m_sub:
        major = m_sub.group(1)
        minor = m_sub.group(2)
        title = m_sub.group(3).strip()
        emit(f'<h3 class="subcategoria" id="sub-{major}-{minor}">Subcategoria {major}.{minor} — {esc(title)}</h3>')
        i += 1
        continue

    # Produto: ### Nome
    if s.startswith('### ') and not s.startswith('### Subcategoria ') and not s.startswith('### Categoria '):
        name = s[4:].strip()
        i += 1
        block, i = collect_product_block(i)
        emit(render_product_block(name, block))
        continue

    # Pack/Linha inline: **Nome** sozinho na linha (sem ":")
    mp = pack_inline_re.match(s)
    if mp and ':' not in mp.group(1):
        name = mp.group(1).strip()
        i += 1
        block, i = collect_product_block(i)
        emit(render_product_block(name, block, is_pack=True))
        continue

    # Blockquote (intro de categoria/subcategoria)
    if s.startswith('>'):
        block = []
        while i < n and lines[i].lstrip().startswith('>'):
            block.append(lines[i].lstrip()[1:].lstrip())
            i += 1
        joined = ' '.join(b for b in block if b)
        if joined:
            emit(f'<p class="note">{inline(joined)}</p>')
        continue

    # Top-level ## (Seccao 1, Nota final, etc)
    if s.startswith('## '):
        title = s[3:].strip()
        if title.startswith('Hero'):
            # ja consumido
            i += 1
            continue
        if title == 'SEO':
            break
        # Emit categorias TOC if title is "Catalogo" — handled above by # Catalogo
        sid = slugify(title)
        emit(f'<h2 id="{sid}">{esc(title)}</h2>')
        i += 1
        continue

    # # heading
    if s.startswith('# '):
        # Skip front-matter title and other top H1 (besides Catalogo, handled)
        i += 1
        continue

    # Numbered list
    if re.match(r'^\d+\.\s', s):
        items = []
        while i < n and re.match(r'^\d+\.\s', lines[i].strip()):
            items.append(re.sub(r'^\d+\.\s', '', lines[i].strip()))
            i += 1
        emit('<ol>')
        for it in items:
            emit(f'  <li>{inline(it)}</li>')
        emit('</ol>')
        continue

    # Bullet list
    if s.startswith('- '):
        items = []
        while i < n and lines[i].strip().startswith('- '):
            items.append(lines[i].strip()[2:])
            i += 1
        emit('<ul>')
        for it in items:
            emit(f'  <li>{inline(it)}</li>')
        emit('</ul>')
        continue

    # HR
    if s == '---':
        i += 1
        continue

    # Blank
    if not s:
        i += 1
        continue

    # Plain paragraph
    para = [s]
    i += 1
    while i < n and lines[i].strip() and not lines[i].lstrip().startswith(('#', '-', '>', '|')) and not re.match(r'^\d+\.\s', lines[i].strip()) and lines[i].strip() != '---':
        para.append(lines[i].rstrip())
        i += 1
    joined = ' '.join(para).strip()
    if joined:
        emit(f'<p>{inline(joined)}</p>')

# Final voltar ao topo
if current_cat is not None:
    emit('<p class="note"><a href="#topo">Voltar ao topo</a> · <a href="#categorias">Ver todas as categorias</a></p>')

# Compose final
out.extend(out_body)

# Footer + back-to-top
out.append('')
out.append('</div>')  # close .page
out.append('')
out.append('<footer>')
out.append('SEO — Meta title: Loja Online | Tratamentos, Vouchers e SPA — Aromas do Deserto<br>')
out.append('Meta description: Reserve protocolos, vouchers SPA, packs de massagem e cartoes presente da Clinica Aromas do Deserto, Braga.<br>')
out.append('Slug: /loja')
out.append('</footer>')
out.append('')
out.append('<a href="#topo" class="back-to-top" aria-label="Voltar ao topo">↑ Topo</a>')
out.append('</body>')
out.append('</html>')

DST.write_text('\n'.join(out), encoding='utf-8')
print(f"OK: {DST}")
print(f"Total produtos-pai: {total_produtos}")
print(f"Categorias: {len(categorias)}")
for c in categorias:
    print(f"  {c['num']:2d}. {c['title']}: {c['count']} produtos")
