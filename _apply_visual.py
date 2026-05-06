"""Aplica refino visual em todos os HTMLs do preview.

Mudancas:
- Adiciona class="active" no link de nav da pagina atual
- Envolve conteudo do <body> em <div class="page"> (entre body e footer)
- Envolve cabecalho (tag + h1 + lead p + cta + note opcional) em <div class="hero">
- Em loja.html: transforma cada par h3 + p em <article class="product"> e extrai preco
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = {
    "index.html":      "index.html",
    "sobre.html":      "sobre.html",
    "metodo.html":     "metodo.html",
    "tratamentos.html":"tratamentos.html",
    "loja.html":       "loja.html",
    "resultados.html": "resultados.html",
    "contacto.html":   "contacto.html",
    "politicas.html":  "politicas.html",
}

def add_nav_active(html: str, current: str) -> str:
    # Adiciona class="active" no <a href="current"> dentro do <nav>
    nav_match = re.search(r"<nav>(.*?)</nav>", html, re.DOTALL)
    if not nav_match:
        return html
    nav = nav_match.group(0)
    new_nav = re.sub(
        r'<a href="' + re.escape(current) + r'"(?![^>]*class)',
        f'<a href="{current}" class="active"',
        nav,
        count=1,
    )
    return html.replace(nav, new_nav, 1)

def wrap_page_container(html: str) -> str:
    """Insere <div class="page"> apos </nav> e </div> antes de <footer>.
    Se nao tiver footer, fecha antes de </body>."""
    if 'class="page"' in html:
        return html  # ja tem
    # depois de </nav>
    if "</nav>" not in html:
        return html
    html = html.replace("</nav>", '</nav>\n\n<div class="page">', 1)
    # antes do <footer ... ou </body>
    if "<footer" in html:
        html = re.sub(r"(\s*)<footer", r"\1</div>\n\n<footer", html, count=1)
    else:
        html = html.replace("</body>", "</div>\n\n</body>", 1)
    return html

def wrap_hero(html: str) -> str:
    """Encontra dentro de <div class="page"> a sequencia:
       <span class="tag">...</span>
       <h1>...</h1>
       <p>...</p>           (lead opcional)
       <div class="cta">..</div>   (opcional)
       <p class="note">..</p>      (opcional)
       e envolve em <div class="hero">.
       Tambem renomeia o primeiro <p> nao-cta para class="lead".
    """
    if 'class="hero"' in html:
        return html

    # Captura bloco do tag ate antes do primeiro <h2 ou <table ou <ol nao-cta
    pattern = re.compile(
        r'(<span class="tag">[\s\S]*?</span>\s*'  # tag
        r'<h1>[\s\S]*?</h1>\s*'                    # h1
        r'(?:<p[^>]*>[\s\S]*?</p>\s*)?'            # lead p (opcional)
        r'(?:<div class="cta">[\s\S]*?</div>\s*)?' # cta opcional
        r'(?:<p class="note">[\s\S]*?</p>\s*)?'    # note opcional
        r')'
    )
    m = pattern.search(html)
    if not m:
        return html
    block = m.group(1)

    # Renomeia primeiro <p> (depois do h1 e antes de cta) para class="lead"
    new_block = re.sub(
        r'(</h1>\s*)<p>([\s\S]*?)</p>',
        r'\1<p class="lead">\2</p>',
        block,
        count=1,
    )
    # Renomeia <p class="placeholder">[FOTO...] inicial -> deixa como esta
    wrapped = f'<div class="hero">\n{new_block.strip()}\n</div>\n'
    return html.replace(block, wrapped, 1)

PRICE_RE = re.compile(r'<strong>Preço:</strong>\s*([^<.]+?)(?=\s*<strong>|\s*\.|\s*$)')
PRICE_RE2 = re.compile(r'<strong>Pre[çc]o:</strong>\s*([^<]+?)(?=<strong>|$)')

def transform_loja_products(html: str) -> str:
    """Em loja.html: pega cada <h3 id=...>...</h3>\n<p>...</p>
    e converte em <article class='product'>...</article>.
    Extrai preco em <span class='price'>."""
    if 'class="product"' in html:
        return html  # idempotencia
    pattern = re.compile(
        r'(<h3 id="[^"]+">[\s\S]*?</h3>)\s*(<p>[\s\S]*?</p>)',
    )
    def repl(m):
        h3 = m.group(1)
        p  = m.group(2)
        # destaca preco: "<strong>Preço:</strong> €120." ou "Preço: Sob consulta..."
        # converte primeiro €valor em <span class="price">€valor</span>
        p2 = re.sub(
            r'(<strong>Pre[çc]o:</strong>)\s*([^<]+?)(?=<strong>|$)',
            lambda mm: mm.group(1) + ' <span class="price">' + mm.group(2).strip().rstrip('.') + '</span>. ',
            p,
            count=1,
        )
        return f'<article class="product">\n{h3}\n{p2}\n</article>'
    return pattern.sub(repl, html)

def add_back_to_top_button(html: str) -> str:
    """Adiciona <a class='back-to-top'> antes de </body> se nao tiver."""
    if 'class="back-to-top"' in html:
        return html
    btn = '<a href="#topo" class="back-to-top" aria-label="Voltar ao topo">↑ Topo</a>\n'
    return html.replace("</body>", btn + "</body>", 1)

def ensure_topo_id(html: str) -> str:
    """Garante id='topo' no body."""
    if 'id="topo"' in html:
        return html
    return html.replace("<body>", '<body id="topo">', 1)

def process(filename: str, current_link: str):
    path = ROOT / filename
    html = path.read_text(encoding="utf-8")
    html = ensure_topo_id(html)
    html = add_nav_active(html, current_link)
    html = wrap_page_container(html)
    html = wrap_hero(html)
    if filename == "loja.html":
        html = transform_loja_products(html)
        html = add_back_to_top_button(html)
    path.write_text(html, encoding="utf-8")
    print(f"OK {filename}")

if __name__ == "__main__":
    for fn, link in PAGES.items():
        process(fn, link)
    print("Done.")
