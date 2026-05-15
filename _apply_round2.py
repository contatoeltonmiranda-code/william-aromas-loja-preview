"""Round 2: dados reais + TEN Science + condicoes + produtos fisicos + footer global."""
import os
import re
import io

PREVIEW = os.path.dirname(os.path.abspath(__file__))

# === FOOTER GLOBAL (contato real) ===
SITE_FOOTER = '''<section class="site-contact">
  <div class="site-contact-grid">
    <div class="site-contact-col">
      <h4>Clínica</h4>
      <p>Rua José António Cruz, N.º 197 R/C<br>S. Vítor · 4715-343 Braga</p>
      <p><a href="https://www.google.com/maps?q=41.545170,-8.405386" target="_blank" rel="noopener">Ver no Google Maps</a></p>
    </div>
    <div class="site-contact-col">
      <h4>Contacto</h4>
      <p>Tel.: <a href="tel:+351253284864">253 284 864</a><br>
      WhatsApp: <a href="https://wa.me/351913468193" target="_blank" rel="noopener">+351 913 468 193</a><br>
      Email: <a href="mailto:reservas@aromasdodeserto.pt">reservas@aromasdodeserto.pt</a></p>
    </div>
    <div class="site-contact-col">
      <h4>Horário</h4>
      <p>Ter–Qui · 10h–13h / 14h–20h<br>
      Sex · 10h–14h / 14h–20h<br>
      Sáb · 9h–13h / 14h–18h<br>
      Dom–Seg · Encerrado</p>
    </div>
    <div class="site-contact-col">
      <h4>Redes</h4>
      <p><a href="https://instagram.com/aromasdodeserto" target="_blank" rel="noopener">Instagram @aromasdodeserto</a><br>
      <a href="https://facebook.com/aromasdodeserto" target="_blank" rel="noopener">Facebook @aromasdodeserto</a></p>
      <p class="site-contact-note">Marcações de serviços apenas via email.</p>
    </div>
  </div>
</section>
'''


def inject_site_footer(html: str) -> str:
    """Insere SITE_FOOTER imediatamente antes de <footer> (a faixa SEO).
    Se ja existir, substitui."""
    # remove anterior
    html = re.sub(r'<section class="site-contact">.*?</section>\s*', '', html, flags=re.DOTALL)
    return html.replace('<footer>', SITE_FOOTER + '\n<footer>', 1)


def apply_contacto(path):
    new = '''<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Contacto | Clínica Aromas do Deserto — Braga</title>
<meta name="description" content="Marque a sua Avaliação Estratégica gratuita. Contacte a Clínica Aromas do Deserto em Braga via WhatsApp (+351 913 468 193), telefone (253 284 864) ou email reservas@aromasdodeserto.pt.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body id="topo">

<nav>
  <a href="index.html">Home</a>
  <a href="sobre.html">Sobre</a>
  <a href="metodo.html">Método</a>
  <a href="tratamentos.html">Tratamentos</a>
  <a href="loja.html">Loja</a>
  <a href="resultados.html">Resultados</a>
  <a href="contacto.html" class="active">Contacto</a>
  <a href="politicas.html">Políticas</a>
</nav>

<div class="page">

<div class="hero">
<span class="tag">Contacto · Clínica Aromas do Deserto · Braga</span>
<h1>Vamos conversar sobre si.</h1>
<p class="lead">Marque a sua Avaliação Estratégica gratuita ou esclareça qualquer questão. A nossa equipa responde com brevidade.</p>
<div class="cta">
  <a href="https://wa.me/351913468193" target="_blank" rel="noopener">Falar via WhatsApp</a>
  <a href="#formulario">Enviar mensagem</a>
</div>
</div>

<h2>Como podemos ajudar</h2>
<p>Quer agendar uma Avaliação Estratégica, conhecer um protocolo específico ou oferecer um cartão presente SPA? Estamos disponíveis para si.</p>
<p>A forma mais rápida de tirar dúvidas é via WhatsApp.</p>
<div class="callout callout-warn">
  <strong>Importante:</strong> as marcações de serviços são realizadas <strong>obrigatoriamente via email</strong> — <a href="mailto:reservas@aromasdodeserto.pt">reservas@aromasdodeserto.pt</a>.
</div>

<h2>Vias de contacto</h2>
<div class="contact-cards">

  <article class="contact-card">
    <h3>WhatsApp</h3>
    <p>Resposta rápida durante o horário de funcionamento.</p>
    <p class="contact-line"><strong>+351 913 468 193</strong></p>
    <p class="cta-line"><a href="https://wa.me/351913468193" target="_blank" rel="noopener">Abrir conversa →</a></p>
  </article>

  <article class="contact-card">
    <h3>Telefone</h3>
    <p>Atendimento direto durante o horário de funcionamento.</p>
    <p class="contact-line"><strong>253 284 864</strong></p>
    <p class="cta-line"><a href="tel:+351253284864">Ligar agora →</a></p>
  </article>

  <article class="contact-card">
    <h3>Email</h3>
    <p>Para marcações de serviços, parcerias e questões detalhadas.</p>
    <p class="contact-line"><strong>reservas@aromasdodeserto.pt</strong></p>
    <p class="contact-sub">www.aromasdodeserto.pt</p>
    <p class="cta-line"><a href="mailto:reservas@aromasdodeserto.pt">Enviar email →</a></p>
  </article>

  <article class="contact-card">
    <h3>Localização</h3>
    <p>Visite-nos na clínica em S. Vítor, Braga.</p>
    <p class="contact-line"><strong>Rua José António Cruz, N.º 197 R/C</strong><br>S. Vítor · 4715-343 Braga</p>
    <p class="contact-sub">GPS · 41.545170, -8.405386</p>
    <p class="cta-line"><a href="https://www.google.com/maps?q=41.545170,-8.405386" target="_blank" rel="noopener">Ver no Google Maps →</a></p>
  </article>

</div>

<h2 id="formulario">Prefere que entremos em contacto consigo?</h2>
<p>Preencha o formulário abaixo e responderemos no próximo horário de funcionamento.</p>
<ul>
  <li>Nome completo*</li>
  <li>Email*</li>
  <li>Telemóvel / WhatsApp*</li>
  <li>Assunto (Avaliação Estratégica · Tratamento específico · Cartão Presente · Outra questão)</li>
  <li>Mensagem*</li>
  <li>Aceitação da Política de Privacidade (RGPD) — checkbox obrigatório</li>
</ul>
<p><strong>Botão:</strong> Enviar mensagem</p>
<p class="note">Os seus dados são protegidos de acordo com o RGPD. Só utilizamos as suas informações para responder ao seu contacto. Marcações de serviços apenas via <a href="mailto:reservas@aromasdodeserto.pt">reservas@aromasdodeserto.pt</a>.</p>

<h2>Estamos aqui para si</h2>
<table>
  <tr><th>Dia</th><th>Horário</th></tr>
  <tr><td>Domingo</td><td>Encerrado</td></tr>
  <tr><td>Segunda</td><td>Encerrado</td></tr>
  <tr><td>Terça</td><td>10h00 – 13h00 / 14h00 – 20h00</td></tr>
  <tr><td>Quarta</td><td>10h00 – 13h00 / 14h00 – 20h00</td></tr>
  <tr><td>Quinta</td><td>10h00 – 13h00 / 14h00 – 20h00</td></tr>
  <tr><td>Sexta</td><td>10h00 – 14h00 / 14h00 – 20h00</td></tr>
  <tr><td>Sábado</td><td>9h00 – 13h00 / 14h00 – 18h00</td></tr>
</table>

<h2 id="mapa">Encontre-nos em Braga</h2>
<p>Rua José António Cruz, N.º 197 R/C — S. Vítor · 4715-343 Braga, Portugal<br>
<strong>GPS:</strong> 41.545170, -8.405386</p>

<div class="map-embed">
  <iframe
    src="https://www.google.com/maps?q=41.545170,-8.405386&hl=pt-PT&z=17&output=embed"
    width="100%" height="380" style="border:0; border-radius:4px;"
    allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
    title="Mapa — Clínica Aromas do Deserto, Braga"></iframe>
</div>

<h2>Acompanhe-nos</h2>
<ul>
  <li>Instagram: <a href="https://instagram.com/aromasdodeserto" target="_blank" rel="noopener">@aromasdodeserto</a></li>
  <li>Facebook: <a href="https://facebook.com/aromasdodeserto" target="_blank" rel="noopener">@aromasdodeserto</a></li>
</ul>

<h2>O que acontece depois de nos contactar?</h2>
<ol>
  <li><strong>Recebemos a sua mensagem</strong> — Respondemos durante o horário de funcionamento.</li>
  <li><strong>Marcamos a Avaliação Estratégica</strong> — Sem custo. Sem compromisso de aquisição.</li>
  <li><strong>Avaliação personalizada</strong> — Análise do seu caso e proposta clara.</li>
  <li><strong>Decisão informada</strong> — Decide com toda a informação na mão.</li>
</ol>

</div>

__SITE_FOOTER__

<footer>
SEO — Meta title: Contacto | Clínica Aromas do Deserto — Braga<br>
Meta description: Marque a sua Avaliação Estratégica gratuita. Contacte a Clínica Aromas do Deserto em Braga via WhatsApp (+351 913 468 193), telefone (253 284 864) ou email reservas@aromasdodeserto.pt.<br>
Slug: /contacto
</footer>

</body>
</html>
'''
    new = new.replace('__SITE_FOOTER__', SITE_FOOTER)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(new)
    return True


def apply_sobre(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1) Trocar Shield Summer -> SaFit Slim (na linha de criadora autoral)
    html = html.replace(
        'desenvolveu métodos autorais como Sá Fit &amp; Regenera e Shield Summer',
        'desenvolveu métodos autorais como Sá Fit &amp; Regenera e SaFit Slim'
    )
    html = html.replace(
        'Criadora do protocolo Shield Summer',
        'Criadora do protocolo SaFit Slim'
    )

    # 2) Substituir a secao das marcas (3 cards) por 4 cards no grid
    marcas_old_pattern = re.compile(
        r'<h2>Cada parceria é uma escolha científica</h2>.*?(?=<h2>O nosso compromisso</h2>)',
        flags=re.DOTALL
    )
    marcas_new = '''<h2>Cada parceria é uma escolha científica</h2>
<p>Acreditamos que a estética só faz sentido quando caminha de mãos dadas com a ciência. Por isso, escolhemos cuidadosamente marcas que defendem a fisiologia do corpo e a regeneração celular.</p>

<div class="brand-grid">

  <article class="brand-card">
    <h3>Dr Irena Eris<span class="brand-loc">Polónia</span></h3>
    <p>Marca europeia de dermocosmética avançada que une investigação científica, biotecnologia e luxo profissional. Os seus protocolos combinam ativos biomiméticos, antioxidantes e tecnologia celular para promover regeneração, proteção e rejuvenescimento cutâneo de forma inteligente e personalizada.</p>
  </article>

  <article class="brand-card">
    <h3>pHformula<span class="brand-loc">Barcelona</span></h3>
    <p>Referência mundial em resurfacing dermatológico médico-estético. Atua profundamente na fisiologia da pele através de uma abordagem regenerativa que estimula renovação celular, equilíbrio cutâneo e reparação da pele, em vez de tratar apenas a superfície.</p>
  </article>

  <article class="brand-card">
    <h3>Ferrari Professional<span class="brand-loc">Itália</span></h3>
    <p>Especializada em ciência regenerativa e bioestimulação celular avançada. Os protocolos integram peelings inteligentes, exossomas, PDRN e ativos biotecnológicos focados na regeneração tecidular, ativação mitocondrial e rejuvenescimento fisiológico da pele.</p>
  </article>

  <article class="brand-card">
    <h3>TEN Science<span class="brand-loc">Itália</span></h3>
    <p>Marca italiana profissional que alia ciência, tecnologia e ingredientes naturais em protocolos de rosto e corpo altamente eficazes. Focada na regeneração, hidratação e firmeza cutânea, a TEN Science trabalha a pele de forma global, promovendo equilíbrio, vitalidade e resultados duradouros.</p>
  </article>

</div>

'''
    html = marcas_old_pattern.sub(marcas_new, html)

    # 3) Inject footer
    html = inject_site_footer(html)

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def apply_index(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1) Faixa de prova social - adicionar TEN Science
    html = html.replace(
        '<li>Ferrari Professional</li>\n  <li>Formação com Dr Carlos Ruiz e Ana Santarelli</li>',
        '<li>Ferrari Professional (Itália)</li>\n  <li>TEN Science (Itália)</li>\n  <li>Formação com Dr Carlos Ruiz e Ana Santarelli</li>'
    )

    # 2) Trocar Shield Summer -> SaFit Slim em autoria Sonia
    html = html.replace(
        'autora de métodos como Sá Fit &amp; Regenera e Shield Summer',
        'autora de métodos como Sá Fit &amp; Regenera e SaFit Slim'
    )

    # 3) Inject footer
    html = inject_site_footer(html)

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


# === LOJA ===
CONDICOES_BLOCK = '''<aside class="conditions-box" id="condicoes">
  <h3>Condições gerais aplicáveis aos serviços</h3>
  <ul>
    <li>Marcações realizadas <strong>obrigatoriamente via email</strong> — <a href="mailto:reservas@aromasdodeserto.pt">reservas@aromasdodeserto.pt</a>.</li>
    <li>Sujeito a marcação prévia e disponibilidade de agenda.</li>
    <li>Cancelamento gratuito com <strong>48 horas de antecedência</strong>.</li>
    <li>A não comparência em sessão marcada resultará na impossibilidade de realização do serviço e na perda do respetivo valor pago.</li>
    <li>Validade máxima de <strong>6 meses</strong> para a realização do serviço adquirido, a contar da data de compra.</li>
  </ul>
  <p class="conditions-note">Estas condições <strong>não se aplicam</strong> a produtos físicos (cosmética profissional). Produtos físicos seguem política padrão de venda e devolução de retalho.</p>
</aside>
'''


PRODUTOS_FISICOS_BLOCK = '''<h2 id="produtos-fisicos">Produtos Físicos — Cosmética Profissional</h2>
<p>A ciência da nossa cabine, agora no seu lavatório. Os mesmos produtos profissionais que prolongam os resultados dos nossos protocolos, selecionados por Sónia Sá.</p>
<p class="note">As <a href="#condicoes">Condições gerais de serviços</a> não se aplicam aos produtos físicos.</p>

<ol class="prod-toc">
  <li><a href="#prod-irena">Dr Irena Eris <span class="cat-count">(21)</span></a></li>
  <li><a href="#prod-karaja">Karaja <span class="cat-count">(5)</span></a></li>
  <li><a href="#prod-phformula">pHformula <span class="cat-count">(21)</span></a></li>
  <li><a href="#prod-tenscience">TEN Science <span class="cat-count">(em breve)</span></a></li>
</ol>

<h3 id="prod-irena" class="subcategoria">Dr Irena Eris — Polónia</h3>
<p>Dermocosmética avançada de alta tecnologia. Rosto e maquilhagem profissional.</p>

<article class="product product-fisico">
  <h3>IR619 — Micellar Complex Gel</h3>
  <p class="price-line"><span class="price-tag">€28,54</span> · 200 ml · Higienização / Rosto</p>
  <p>Gel de limpeza de alta tecnologia que remove maquilhagem e impurezas sem comprometer a barreira hidrolipídica. 11% de micelas para eficácia notável. Adequado a peles sensíveis.</p>
</article>

<article class="product product-fisico">
  <h3>IR849 — Art Lifting Serum Instantâneo Dia</h3>
  <p class="price-line"><span class="price-tag">€91,34</span> · 30 ml · Sérum / Anti-idade</p>
  <p>Sérum diurno com Advanced MultiPeptide e Complexo Promatrix. Efeito lifting imediato, redução de rugas e hidratação intensiva em três níveis da pele.</p>
</article>

<article class="product product-fisico">
  <h3>ART 848 — High Restore Therapy Night</h3>
  <p class="price-line"><span class="price-tag">€89,24</span> · 50 ml · Creme de Noite / Anti-idade</p>
  <p>Creme reparador noturno com complexo PCL-Lift-Up. Restaura volume facial, preenche linhas e estimula colagénio em profundidade durante o sono.</p>
</article>

<article class="product product-fisico">
  <h3>IR847 — Art Lifting Creme Renovador Dia FPS 30</h3>
  <p class="price-line"><span class="price-tag">€85,04</span> · 50 ml · Creme de Dia / Anti-idade</p>
  <p>Lifting, bio-modelagem do oval facial e preenchimento multidimensional de rugas. Proteção solar FPS 30 integrada.</p>
</article>

<article class="product product-fisico">
  <h3>Aqua Idealine 872 — Ultra Moisturizing Face Mask</h3>
  <p class="price-line"><span class="price-tag">€70,66</span> · 50 ml · Máscara Hidratante / Noite</p>
  <p>Máscara ultraleve com Hidrocomplexo Probiotix-PGA. Hidratação 4× superior ao ácido hialurónico e fortalecimento da barreira cutânea.</p>
</article>

<article class="product product-fisico">
  <h3>Aqua Idealine 873 — Moisturizing Face Booster</h3>
  <p class="price-line"><span class="price-tag">€75,18</span> · 30 ml · Sérum / Hidratação</p>
  <p>Sérum dia/noite que alisa a epiderme em segundos. Estimula produção do Fator Natural de Hidratação e lípidos do cimento intercelular.</p>
</article>

<article class="product product-fisico">
  <h3>Aqua Idealine 871 — Creme Hidratante Probiótico Dia FPS 30</h3>
  <p class="price-line"><span class="price-tag">€69,34</span> · 50 ml · Creme de Dia / Hidratação</p>
  <p>Hidratação probiótica com algas vermelhas e folha de oliveira. Efeito lifting natural e fotoproteção FPS 30.</p>
</article>

<article class="product product-fisico">
  <h3>IR851 — Capill Age Creme Facial Alisante e Fortalecedor</h3>
  <p class="price-line"><span class="price-tag">€72,44</span> · 50 ml · Pele Sensível com Capilares</p>
  <p>Formulado para pele com vasos visíveis. Reduz vermelhidão em 31% e visibilidade vascular em 83% em 4 semanas. FPS 20.</p>
</article>

<article class="product product-fisico">
  <h3>IR852 — Capill Age Creme de Noite Anti-rugas</h3>
  <p class="price-line"><span class="price-tag">€74,54</span> · 50 ml · Creme de Noite / Pele Sensível</p>
  <p>Regeneração noturna para peles vasculares. Vitamina K única e hesperidina fortalecem vasos e uniformizam o tom.</p>
</article>

<article class="product product-fisico">
  <h3>IR853 — Capill Age Concentrado Rejuvenescedor Dia</h3>
  <p class="price-line"><span class="price-tag">€65,00</span> · 30 ml · Primeiros Sinais</p>
  <p>Para os primeiros sinais de envelhecimento com sensibilidade vascular. Complexo PuriOlea e diosmina. Resultados em 4 semanas.</p>
</article>

<article class="product product-fisico">
  <h3>IR855 — Capill Age Pro Capilar Repair Sérum</h3>
  <p class="price-line"><span class="price-tag">€93,44</span> · 30 ml · Sérum / Pele Vascular</p>
  <p>Ultra-intensivo. Reduz visibilidade de capilares em 90% e aumenta firmeza em 74% em 4 semanas.</p>
</article>

<article class="product product-fisico">
  <h3>Ultra C Regeniq 857 — Active Rejuvenating Day Cream SPF 30</h3>
  <p class="price-line"><span class="price-tag">€85,06</span> · 50 ml · Creme de Dia / Antioxidante</p>
  <p>Vitamina C estabilizada da ameixa Kakadu. Estimula colagénio e ácido hialurónico. Fotoproteção FPS 30.</p>
</article>

<article class="product product-fisico">
  <h3>Ultra C Regeniq 858 — Repairing &amp; Rejuvenating Night Cream</h3>
  <p class="price-line"><span class="price-tag">€87,48</span> · 50 ml · Creme de Noite / Antioxidante</p>
  <p>Reparação noturna celular com ameixa Kakadu, hexapéptido e edelweiss orgânico. Antioxidante intensivo.</p>
</article>

<h4 class="subcategoria-min">Maquilhagem Dr Irena Eris</h4>

<article class="product product-fisico">
  <h3>Day to Night Longwear Coverage Foundation SPF 30</h3>
  <p class="price-line"><span class="price-tag">€62,00</span> · Tons: 040C Honey / 040W Natural / 050W Carmel</p>
  <p>Base de cobertura prolongada com acabamento liso. Duração até 24 horas e FPS 30.</p>
</article>

<article class="product product-fisico">
  <h3>Flawless Skin Anti-Aging Foundation Smooth &amp; Firm SPF 30</h3>
  <p class="price-line"><span class="price-tag">€44,00</span> · Tons: 040C Honey / 050W Carmel</p>
  <p>Base para pele madura. Cobertura premium com cuidado anti-rugas integrado. FPS 30.</p>
</article>

<article class="product product-fisico">
  <h3>Urban Glow Luminous Anti-Pollution Foundation SPF 30</h3>
  <p class="price-line"><span class="price-tag">€46,74</span> · Tons: 030W Golden / 040C Honey</p>
  <p>Cobertura média luminosa, acabamento acetinado. Proteção anti-poluição urbana e FPS 30.</p>
</article>

<article class="product product-fisico">
  <h3>BB Cream Waterproof SPF 50</h3>
  <p class="price-line"><span class="price-tag">€51,00</span> · Tom: N40 — Bege Quente Universal</p>
  <p>BB Cream resistente à água com proteção FPS 50. Ideal para atividade física.</p>
</article>

<article class="product product-fisico">
  <h3>Extreme Volume Mascara Black</h3>
  <p class="price-line"><span class="price-tag">€29,00</span> · Pestanas / Volume</p>
  <p>Volume dramático em preto intenso. Protect Lash Complex nutre as pestanas. Testada dermatologicamente.</p>
</article>

<article class="product product-fisico">
  <h3>Perfect Lashes Mascara 3in1</h3>
  <p class="price-line"><span class="price-tag">A confirmar</span> · Pestanas / Multifuncional</p>
  <p>Volume, comprimento e curvatura num só gesto. Complexo Forming. Testada dermatologicamente.</p>
</article>

<article class="product product-fisico">
  <h3>Long Lashes Mascara Black</h3>
  <p class="price-line"><span class="price-tag">€29,00</span> · Pestanas / Comprimento</p>
  <p>Alongamento intenso em preto profundo e brilhante. Complexo Shellac e cera natural.</p>
</article>

<article class="product product-fisico">
  <h3>Ultimate Shine Lip Gloss (10 tons)</h3>
  <p class="price-line"><span class="price-tag">€22,90 – €27,48</span> · Lábios / Brilho Nutritivo</p>
  <p>Brilho labial condicionante com óleos de macadâmia, jojoba e argão. 10 tons: Cool Pink, Honey Nude, Dusty Peach, Wedding Pink, Sweet Fuchsia, Juicy Coral, Seductive Red, Oh Carmine, Firm Plum, Give'em Sparkle.</p>
</article>

<h3 id="prod-karaja" class="subcategoria">Karaja — Itália</h3>
<p>Maquilhagem cosmecêutica italiana. Fórmulas que cuidam enquanto embelezam.</p>

<article class="product product-fisico">
  <h3>K-Wish Set</h3>
  <p class="price-line"><span class="price-tag">€39,00</span> · Coffret Presente</p>
  <p>Rímel + Esfoliante labial + Batom + Oferta Gloss vermelho. Três produtos icónicos numa caixa-presente.</p>
</article>

<article class="product product-fisico">
  <h3>Lápis Corretivo — N1 (claro)</h3>
  <p class="price-line"><span class="price-tag">€12,00</span> · Maquilhagem / Correção</p>
  <p>Corretor multiuso de formulação cremosa. Acabamento mate aveludado. Tom claro universal.</p>
</article>

<article class="product product-fisico">
  <h3>Lápis Corretivo — N2 (escuro)</h3>
  <p class="price-line"><span class="price-tag">€12,00</span> · Maquilhagem / Correção</p>
  <p>Versão para tons médios e escuros. Fácil de esbater, ideal para pontos estratégicos.</p>
</article>

<article class="product product-fisico">
  <h3>Photo Finish (4 tons)</h3>
  <p class="price-line"><span class="price-tag">€29,00</span> · 30 ml · Base / Efeito Lifting</p>
  <p>Acabamento mate fotográfico com efeito lifting. Tons N30, N50, N60, N90. Ideal para peles mistas e oleosas.</p>
</article>

<article class="product product-fisico">
  <h3>Skin Velvet (2 tons)</h3>
  <p class="price-line"><span class="price-tag">€29,00</span> · 27 ml · Base / Pele Normal a Seca</p>
  <p>Acabamento aveludado radiante com proteção anti-envelhecimento. Tons N3 e N5 (esgotado).</p>
</article>

<h3 id="prod-phformula" class="subcategoria">pHformula — Barcelona</h3>
<p>Resurfacing dermatológico médico-estético. Linha profissional agora em casa.</p>

<article class="product product-fisico">
  <h3>C.C. Cream SPF30</h3>
  <p class="price-line"><span class="price-tag">€50,00</span> · 50 ml · CC Cream / Fotoproteção</p>
  <p>CC Cream vegan-friendly em 4 tons (Light, Light-Medium, Medium, Dark). Filtros amigos dos recifes. Adequado durante a gravidez.</p>
</article>

<article class="product product-fisico">
  <h3>E.X.F.O. Cleanse 200 ml</h3>
  <p class="price-line"><span class="price-tag">€50,50</span> · 200 ml · Limpeza / Esfoliação Suave</p>
  <p>Limpeza hidratante com esfoliação suave diária. Ideal pós-tratamentos profissionais. Sem parabenos.</p>
</article>

<article class="product product-fisico">
  <h3>E.Y.E. Recovery</h3>
  <p class="price-line"><span class="price-tag">€69,00</span> · 20 ml · Contorno Ocular / Anti-idade</p>
  <p>Bakuchiol — alternativa suave ao Retinol. Reduz rugas, olheiras e papos sem irritação.</p>
</article>

<article class="product product-fisico">
  <h3>PH013 — E.X.F.O. Cleanse 100 ml</h3>
  <p class="price-line"><span class="price-tag">€29,67</span> · 100 ml · Limpeza Compacta</p>
  <p>Formato de viagem da limpeza profissional pHformula. Mesma fórmula da versão 200 ml.</p>
</article>

<article class="product product-fisico">
  <h3>PH018 — P.O.S.T. Recovery Cream</h3>
  <p class="price-line"><span class="price-tag">€47,60</span> · 50 ml · Pós-Tratamento</p>
  <p>Recuperação suave após resurfacing profissional. Acalma e hidrata durante a regeneração.</p>
</article>

<article class="product product-fisico">
  <h3>P.O.W.E.R. Essence Tonic</h3>
  <p class="price-line"><span class="price-tag">€45,50</span> · Tónico / Preparador</p>
  <p>Tónico facial avançado. Hidrata, revitaliza e potencia absorção dos cuidados seguintes.</p>
</article>

<article class="product product-fisico">
  <h3>Sérum Corretivo Concentrado VITA C</h3>
  <p class="price-line"><span class="price-tag">€61,00</span> · 30 ml · Sérum / Iluminador</p>
  <p>Vitamina C com comunicação célula a célula. Trata fotoenvelhecimento e hidrata profundamente.</p>
</article>

<article class="product product-fisico">
  <h3>Sérum Corretivo Concentrado HYDRA</h3>
  <p class="price-line"><span class="price-tag">€73,92</span> · 30 ml · Sérum / Hidratação Profunda</p>
  <p>Hidratação multinível para camadas mais profundas. Adequado a pele sensível e todas as idades.</p>
</article>

<article class="product product-fisico">
  <h3>Sérum Corretivo Concentrado MELA</h3>
  <p class="price-line"><span class="price-tag">€76,65</span> · 30 ml · Sérum / Anti-Manchas</p>
  <p>Atenua hiperpigmentação, uniformiza tom. Atua no fotoenvelhecimento e melasma.</p>
</article>

<article class="product product-fisico">
  <h3>SPOT ON Moisture Balance</h3>
  <p class="price-line"><span class="price-tag">€44,10</span> · 50 ml · Hidratante / Pele Mista a Oleosa</p>
  <p>Hidratação leve com acabamento mate. Reduz aparência de poros e refina textura.</p>
</article>

<article class="product product-fisico">
  <h3>N.E.C.K. Recovery</h3>
  <p class="price-line"><span class="price-tag">€73,98</span> · 50 ml · Pescoço &amp; Decote</p>
  <p>Cuidado específico para pescoço, decote e zona dos seios. Misturas biotecnológicas avançadas.</p>
</article>

<article class="product product-fisico">
  <h3>MESO X Boost</h3>
  <p class="price-line"><span class="price-tag">€75,00</span> · 30 ml · Microagulhamento Líquido</p>
  <p>Microagulhamento líquido para uso doméstico. Exossomas biomiméticos e complexo quíntuplo de ácido hialurónico.</p>
</article>

<article class="product product-fisico">
  <h3>VITA A Cream</h3>
  <p class="price-line"><span class="price-tag">€78,60</span> · 50 ml · Retinol Avançado</p>
  <p>Complexo Retinol 1,5% com duplo antioxidante. Renovação celular intensiva e hidratação 24h.</p>
</article>

<article class="product product-fisico">
  <h3>VITA B3 Cream</h3>
  <p class="price-line"><span class="price-tag">€65,10</span> · 50 ml · Niacinamida</p>
  <p>Niacinamida em alta concentração. Reforça barreira, reduz vermelhidão e uniformiza tom.</p>
</article>

<article class="product product-fisico">
  <h3>VITA C Cream</h3>
  <p class="price-line"><span class="price-tag">€78,60</span> · 50 ml · Vitamina C</p>
  <p>Fosfato de Ascorbilo de Magnésio. Antioxidante diário com hidratação 24h.</p>
</article>

<article class="product product-fisico">
  <h3>S.O.S. Hydra Gel Mask</h3>
  <p class="price-line"><span class="price-tag">€30,56</span> · Máscara / Hidratação Calmante</p>
  <p>Resgate imediato para peles secas e irritadas. Ácido hialurónico e raiz de chicória.</p>
</article>

<article class="product product-fisico">
  <h3>DERMABRASION Mild Cream</h3>
  <p class="price-line"><span class="price-tag">€65,90</span> · Esfoliação / Renovação</p>
  <p>Microdermabrasão suave. Pele mais lisa, uniforme e luminosa.</p>
</article>

<article class="product product-fisico">
  <h3>A.G.E. Recovery</h3>
  <p class="price-line"><span class="price-tag">€62,22</span> · Recovery / Anti-idade</p>
  <p>Sinergia com tratamentos pHformula de resurfacing. Anti-idade, fotoenvelhecimento e prevenção.</p>
</article>

<article class="product product-fisico">
  <h3>C.R. Recovery</h3>
  <p class="price-line"><span class="price-tag">€60,35</span> · Recovery / Pele Sensível</p>
  <p>Recuperação dedicada a peles sensíveis e rosácea (ETR). Fortalece defesas naturais.</p>
</article>

<article class="product product-fisico">
  <h3>M.E.L.A. Recovery</h3>
  <p class="price-line"><span class="price-tag">€67,00</span> · Recovery / Anti-Manchas</p>
  <p>Clareamento sem irritação para hiperpigmentação tenaz. Melasma, cloasma, lentigos.</p>
</article>

<article class="product product-fisico">
  <h3>A.C. Recovery</h3>
  <p class="price-line"><span class="price-tag">€59,07</span> · Recovery / Pele Acneica</p>
  <p>Recuperação especializada para acne graus I, II e III. Regula sebo e reduz poros dilatados.</p>
</article>

<h3 id="prod-tenscience" class="subcategoria">TEN Science — Itália</h3>
<p>Ciência italiana aplicada ao corpo, rosto e fotoproteção. Categorias previstas: Corpo, Rosto, Solares.</p>

<article class="product product-fisico product-placeholder">
  <h3>Catálogo em integração</h3>
  <p>A gama TEN Science está em fase de integração no nosso catálogo. Para informações atualizadas sobre disponibilidade e referências, contacte a clínica.</p>
  <p class="cta-line"><a href="mailto:reservas@aromasdodeserto.pt">Pedir lista de produtos →</a></p>
</article>

<p class="note"><a href="#produtos-fisicos">Voltar ao início dos produtos físicos</a> · <a href="#topo">Topo da página</a></p>

'''


def apply_loja(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1) Inserir bloco de Condicoes logo antes do "Secao 1 - Como funciona a compra"
    # Remove se ja existir
    html = re.sub(
        r'<aside class="conditions-box".*?</aside>\s*',
        '', html, flags=re.DOTALL
    )
    html = html.replace(
        '<h2 id="seccao-1-como-funciona-a-compra">Secção 1 — Como funciona a compra</h2>',
        CONDICOES_BLOCK + '\n<h2 id="seccao-1-como-funciona-a-compra">Secção 1 — Como funciona a compra</h2>'
    )

    # 2) Inserir bloco de Produtos Fisicos antes do </div> antes do <footer>
    # Remove se ja existir
    html = re.sub(
        r'<h2 id="produtos-fisicos">.*?(?=</div>\s*\n*<footer>)',
        '', html, flags=re.DOTALL
    )
    html = html.replace(
        '</div>\n\n<footer>',
        PRODUTOS_FISICOS_BLOCK + '\n</div>\n\n' + SITE_FOOTER + '\n<footer>',
        1
    )

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def apply_simple_footer(path):
    """Para metodo, tratamentos, resultados, politicas: so injeta SITE_FOOTER."""
    with io.open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_site_footer(html)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


# === CSS adicional ===
CSS_EXTRA = '''
/* ===== Round 2 — contato, marcas, condicoes, produtos fisicos ===== */

/* Callout (aviso) */
.callout {
  border-left: 3px solid var(--accent);
  background: var(--surface);
  padding: 1rem 1.4rem;
  margin: 1.4rem 0;
  font-size: 0.97rem;
}
.callout-warn { border-left-color: var(--accent); }
.callout strong { color: var(--ink); }

/* Cards de contato */
.contact-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  margin: 1.5rem 0 2.5rem;
}
.contact-card {
  background: var(--surface);
  border-left: 3px solid var(--accent);
  padding: 1.4rem 1.6rem;
  border-radius: 4px;
}
.contact-card h3 {
  margin: 0 0 0.5rem;
  font-family: var(--sans);
  font-size: 1.1rem;
  color: var(--ink);
}
.contact-card p { margin: 0.35rem 0; }
.contact-card .contact-line { font-size: 1.02rem; color: var(--ink); }
.contact-card .contact-sub { color: var(--muted); font-size: 0.88rem; }
.contact-card .cta-line { margin-top: 0.8rem; font-size: 0.95rem; }
.contact-card .cta-line a {
  color: var(--accent);
  font-weight: 500;
  text-decoration: none;
  border-bottom: 1px solid var(--accent-soft);
}
.contact-card .cta-line a:hover { border-bottom-color: var(--ink); color: var(--ink); }

@media (max-width: 640px) {
  .contact-cards { grid-template-columns: 1fr; gap: 1rem; }
}

/* Mapa embed */
.map-embed {
  margin: 1.5rem 0 2.5rem;
  border: 1px solid var(--rule);
  border-radius: 4px;
  overflow: hidden;
  background: var(--surface);
}

/* Grid de marcas (4 colunas desktop, 2 tablet, 1 mobile) */
.brand-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin: 1.5rem 0 2.5rem;
}
.brand-card {
  background: var(--surface);
  border-top: 3px solid var(--accent);
  padding: 1.4rem 1.3rem;
  border-radius: 4px;
}
.brand-card h3 {
  margin: 0 0 0.6rem;
  font-family: var(--serif);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--ink);
  display: flex;
  flex-direction: column;
}
.brand-card .brand-loc {
  display: inline-block;
  font-family: var(--sans);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
  margin-top: 0.2rem;
}
.brand-card p {
  font-size: 0.92rem;
  margin: 0;
  line-height: 1.6;
}
@media (max-width: 980px) { .brand-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .brand-grid { grid-template-columns: 1fr; } }

/* Condicoes gerais (loja) */
.conditions-box {
  background: #fbf3ee;
  border: 1px solid #e8d4c4;
  border-left: 4px solid var(--accent);
  padding: 1.5rem 1.75rem;
  border-radius: 4px;
  margin: 1.5rem 0 2.5rem;
}
.conditions-box h3 {
  margin: 0 0 0.8rem;
  font-family: var(--sans);
  font-size: 1.05rem;
  color: var(--ink);
}
.conditions-box ul { margin: 0; padding-left: 1.2rem; }
.conditions-box li { margin: 0.35rem 0; color: var(--ink-soft); font-size: 0.95rem; }
.conditions-box .conditions-note {
  margin-top: 1rem;
  padding-top: 0.85rem;
  border-top: 1px dashed #d8c0aa;
  color: var(--muted);
  font-size: 0.88rem;
  font-style: italic;
}

/* Produto fisico — variante mais simples */
.product-fisico {
  border-left-color: var(--accent-soft);
}
.product-fisico h3 {
  font-family: var(--sans);
  font-size: 1.05rem;
}
.product-placeholder {
  background: #faf6f1;
  border-left-style: dashed;
}

/* Subcategoria minima (h4 dentro de produtos fisicos) */
.subcategoria-min {
  font-family: var(--sans);
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-muted);
  margin: 2rem 0 1rem;
  font-weight: 600;
}

/* Produtos TOC mini */
.prod-toc {
  background: var(--surface-toc);
  padding: 1.25rem 1.5rem;
  border-radius: 4px;
  list-style: none;
  margin: 1rem 0 2rem;
  padding-left: 1.5rem;
}
.prod-toc li { padding: 0.25rem 0; }
.prod-toc li a { color: var(--ink-soft); text-decoration: none; font-weight: 500; }
.prod-toc li a:hover { color: var(--accent); }

/* Site footer (contato global, antes do bloco SEO) */
.site-contact {
  margin: 5rem 0 0;
  padding: 2.5rem 0 1rem;
  border-top: 1px solid var(--rule);
}
.site-contact-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}
.site-contact-col h4 {
  font-family: var(--sans);
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent);
  margin: 0 0 0.6rem;
}
.site-contact-col p {
  font-size: 0.88rem;
  margin: 0.3rem 0;
  color: var(--ink-soft);
  line-height: 1.55;
}
.site-contact-col a {
  color: var(--ink-soft);
  text-decoration: none;
  border-bottom: 1px solid var(--rule);
}
.site-contact-col a:hover { color: var(--accent); border-bottom-color: var(--accent-soft); }
.site-contact-note {
  font-size: 0.78rem !important;
  font-style: italic;
  color: var(--muted) !important;
  margin-top: 0.6rem !important;
}
@media (max-width: 980px) { .site-contact-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .site-contact-grid { grid-template-columns: 1fr; gap: 1.2rem; } }
'''


def apply_css():
    css_path = os.path.join(PREVIEW, 'assets', 'style.css')
    with io.open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    # marca para evitar duplicar
    marker = '/* ===== Round 2 — contato, marcas, condicoes, produtos fisicos ===== */'
    if marker in css:
        # remove bloco anterior (tudo apos o marker)
        css = css.split(marker)[0].rstrip() + '\n'
    css += '\n' + CSS_EXTRA
    with io.open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)


def main():
    apply_css()

    p_contacto = os.path.join(PREVIEW, 'contacto.html')
    p_sobre = os.path.join(PREVIEW, 'sobre.html')
    p_index = os.path.join(PREVIEW, 'index.html')
    p_loja = os.path.join(PREVIEW, 'loja.html')
    p_metodo = os.path.join(PREVIEW, 'metodo.html')
    p_trat = os.path.join(PREVIEW, 'tratamentos.html')
    p_res = os.path.join(PREVIEW, 'resultados.html')
    p_pol = os.path.join(PREVIEW, 'politicas.html')

    apply_contacto(p_contacto)
    print('[OK] contacto.html')
    apply_sobre(p_sobre)
    print('[OK] sobre.html')
    apply_index(p_index)
    print('[OK] index.html')
    apply_loja(p_loja)
    print('[OK] loja.html')
    apply_simple_footer(p_metodo)
    print('[OK] metodo.html')
    apply_simple_footer(p_trat)
    print('[OK] tratamentos.html')
    apply_simple_footer(p_res)
    print('[OK] resultados.html')
    apply_simple_footer(p_pol)
    print('[OK] politicas.html')


if __name__ == '__main__':
    main()
