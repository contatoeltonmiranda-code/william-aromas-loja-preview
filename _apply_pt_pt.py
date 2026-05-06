"""Aplica revisao ortografica PT-PT (acordo ortografico) nos HTMLs.

Substitui pre-acordo -> pos-acordo. Preserva visual/CSS/estrutura.
Regenera loja.html via _gen_loja.py separadamente.

Pares construidos comparando os 8 .md revisados pela Clara contra os
HTMLs atuais (que estavam em PT-PT pre-acordo de 1990).
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Pares ordenados (formas mais especificas primeiro). Case-sensitive,
# preserva capitalizacao via funcao auxiliar.
PAIRS = [
    # acç -> aç (mas NUNCA em "aceit", "aceiti" -> nao tem 'cc')
    ("acção", "ação"),
    ("acções", "ações"),
    ("Acção", "Ação"),
    ("Acções", "Ações"),
    # activ -> ativ
    ("activação", "ativação"),
    ("Activação", "Ativação"),
    ("activa", "ativa"),
    ("Activa", "Ativa"),
    ("activo", "ativo"),
    ("Activo", "Ativo"),
    ("activos", "ativos"),
    ("Activos", "Ativos"),
    ("activamente", "ativamente"),
    # actua -> atua (cuidado com "actual" que tambem vai)
    ("actua", "atua"),
    ("Actua", "Atua"),
    ("actual", "atual"),
    ("Actual", "Atual"),
    ("actualidade", "atualidade"),
    ("actualização", "atualização"),
    ("Actualização", "Atualização"),
    ("actualmente", "atualmente"),
    ("Actualmente", "Atualmente"),
    ("reactiva", "reativa"),
    ("Reactiva", "Reativa"),
    # factor -> fator
    ("factor", "fator"),
    ("Factor", "Fator"),
    ("factores", "fatores"),
    ("Factores", "Fatores"),
    # factur -> fatur
    ("facturação", "faturação"),
    ("Facturação", "Faturação"),
    ("factura", "fatura"),
    ("Factura", "Fatura"),
    # afect -> afet
    ("afecta", "afeta"),
    ("Afecta", "Afeta"),
    ("afecto", "afeto"),
    ("Afecto", "Afeto"),
    # reflect -> reflet
    ("reflecte", "reflete"),
    ("Reflecte", "Reflete"),
    ("reflectem", "refletem"),
    ("Reflectem", "Refletem"),
    ("reflectir", "refletir"),
    ("Reflectir", "Refletir"),
    # aspect -> aspet
    ("aspecto", "aspeto"),
    ("Aspecto", "Aspeto"),
    ("aspectos", "aspetos"),
    ("Aspectos", "Aspetos"),
    # respect -> respet
    ("respectivo", "respetivo"),
    ("Respectivo", "Respetivo"),
    ("respectivos", "respetivos"),
    ("Respectivos", "Respetivos"),
    ("respectiva", "respetiva"),
    ("Respectiva", "Respetiva"),
    ("respectivamente", "respetivamente"),
    # direcç -> direç
    ("direcção", "direção"),
    ("Direcção", "Direção"),
    # recepç -> receç
    ("recepção", "receção"),
    ("Recepção", "Receção"),
    # excepç -> exceç
    ("excepção", "exceção"),
    ("Excepção", "Exceção"),
    # rectif -> retif
    ("rectificação", "retificação"),
    ("Rectificação", "Retificação"),
    # protecç -> proteç
    ("protecção", "proteção"),
    ("Protecção", "Proteção"),
    # ópti -> óti (ótica)
    ("óptica", "ótica"),
    ("Óptica", "Ótica"),
    # tracç -> traç
    ("tracção", "tração"),
    ("Tracção", "Tração"),
]

# Paginas a processar (loja.html eh regenerada via _gen_loja.py)
PAGES = [
    "index.html",
    "sobre.html",
    "metodo.html",
    "tratamentos.html",
    "resultados.html",
    "contacto.html",
    "politicas.html",
]


def apply_pairs(text: str) -> tuple[str, list[tuple[str, str, int]]]:
    """Aplica todos os pares e retorna (texto_novo, mudancas)."""
    changes = []
    for old, new in PAIRS:
        count = text.count(old)
        if count > 0:
            text = text.replace(old, new)
            changes.append((old, new, count))
    return text, changes


def main():
    total_changes = 0
    for page in PAGES:
        path = ROOT / page
        original = path.read_text(encoding="utf-8")
        new_text, changes = apply_pairs(original)
        if changes:
            path.write_text(new_text, encoding="utf-8")
            total = sum(c[2] for c in changes)
            total_changes += total
            print(f"OK {page} — {total} substituicoes")
            for old, new, n in changes:
                print(f"   {old:30s} -> {new:30s} ({n}x)")
        else:
            print(f"-- {page} — sem alteracoes")

    # Regenera loja.html
    print("\nRegenerando loja.html via _gen_loja.py...")
    result = subprocess.run(
        [sys.executable, str(ROOT / "_gen_loja.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    print(result.stdout)
    if result.returncode != 0:
        print("ERRO:", result.stderr)
        sys.exit(1)

    print(f"\nTotal: {total_changes} substituicoes em {len(PAGES)} ficheiros + loja.html regenerada")


if __name__ == "__main__":
    main()
