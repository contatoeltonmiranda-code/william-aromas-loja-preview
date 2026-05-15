# Round 2.3 — Cards de produtos fisicos expandidos com accordion <details>
# Parse copy/09-produtos-fisicos.md e reescreve bloco em loja.html
# Opcao A: card colapsado mostra nome+preco+headline; <details> expande tudo

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "copy" / "09-produtos-fisicos.md"
HTML = ROOT / "preview" / "loja.html"

raw = MD.read_text(encoding="utf-8")

# Conversao de markdown bold **x** -> <strong>x</strong>  + acentuacao PT-PT
def md_to_html(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"<em>\1</em>", text)
    return apply_pt(text)

# Normalizacao PT-PT pos-acordo (acentos perdidos no MD)
# Substituicoes inteiras-palavra (case sensitive). Aplicada APENAS em texto plain (nao em IDs/anchors).
FIX_MAP = [
    # Acentos comuns que estao faltando no MD fonte
    ("descricao", "descrição"), ("Descricao", "Descrição"),
    ("descricoes", "descrições"), ("Descricoes", "Descrições"),
    ("aplicacao", "aplicação"), ("Aplicacao", "Aplicação"),
    ("aplicacoes", "aplicações"),
    ("acao", "ação"), ("Acao", "Ação"),
    ("acoes", "ações"), ("Acoes", "Ações"),
    ("proteccao", "proteção"), ("Proteccao", "Proteção"),
    ("protecao", "proteção"), ("Protecao", "Proteção"),
    ("seleccao", "seleção"),
    ("hidratacao", "hidratação"), ("Hidratacao", "Hidratação"),
    ("regeneracao", "regeneração"), ("Regeneracao", "Regeneração"),
    ("renovacao", "renovação"),
    ("nutricao", "nutrição"),
    ("inflamacao", "inflamação"),
    ("vermelhidao", "vermelhidão"),
    ("comunicacao", "comunicação"),
    ("circulacao", "circulação"),
    ("microcirculacao", "microcirculação"),
    ("absorcao", "absorção"),
    ("concentracao", "concentração"),
    ("concentracoes", "concentrações"),
    ("formacao", "formação"),
    ("manutencao", "manutenção"),
    ("reparacao", "reparação"),
    ("sensacao", "sensação"),
    ("sensacoes", "sensações"),
    ("solucao", "solução"),
    ("racao", "ração"),
    ("Reducao", "Redução"), ("reducao", "redução"),
    ("educacao", "educação"),
    ("excecao", "exceção"),
    ("posicao", "posição"),
    ("composicao", "composição"),
    ("oposicao", "oposição"),
    ("revisao", "revisão"),
    ("divisao", "divisão"),
    ("decisao", "decisão"),
    ("transmissao", "transmissão"),
    ("transpiracao", "transpiração"),
    ("respiracao", "respiração"),
    ("inspeccao", "inspeção"),
    ("perfeccao", "perfeição"),
    ("perfeicao", "perfeição"),
    ("informacao", "informação"),
    ("transformacao", "transformação"),
    ("estimulacao", "estimulação"),
    ("formulacao", "formulação"),
    ("alteracao", "alteração"), ("alteracoes", "alterações"),
    ("apresentacao", "apresentação"),
    ("calibragem", "calibragem"),
    ("oleos", "óleos"), ("oleo", "óleo"),
    ("labios", "lábios"), ("labial", "labial"),
    ("cilios", "cílios"),
    ("apos", "após"),
    ("alem", "além"),
    ("ate ", "até "),
    ("nao ", "não "), ("Nao ", "Não "),
    ("Sao ", "São "), ("sao ", "são "),
    ("orgao", "órgão"),
    ("colagenio", "colagénio"),
    ("hialuronico", "hialurónico"),
    ("hexapeptideo", "hexapéptido"),
    ("tripeptideo", "tripéptido"),
    ("tetrapeptideo", "tetrapéptido"),
    ("peptido", "péptido"), ("peptidos", "péptidos"),
    ("Peptido", "Péptido"), ("Peptidos", "Péptidos"),
    ("rosacea", "rosácea"),
    ("acido", "ácido"), ("Acido", "Ácido"),
    ("acidos", "ácidos"),
    ("seda ", "seda "),
    ("preco", "preço"), ("Preco", "Preço"),
    ("publico", "público"),
    ("estavel", "estável"),
    ("sensiveis", "sensíveis"), ("sensivel", "sensível"),
    ("Sensivel", "Sensível"),
    ("ciencia", "ciência"), ("Ciencia", "Ciência"),
    ("ciencias", "ciências"),
    ("pesquisa", "pesquisa"),
    ("polaca", "polaca"),
    ("Italia", "Itália"),
    ("alergicas", "alérgicas"), ("alergicos", "alérgicos"),
    ("avancado", "avançado"), ("avancada", "avançada"),
    ("avancadas", "avançadas"), ("avancados", "avançados"),
    ("Avancado", "Avançado"), ("Avancada", "Avançada"),
    ("graca a", "graças a"), ("Graca a", "Graças a"),
    ("graca ", "graça "),
    ("celulas", "células"), ("celula", "célula"),
    ("Celulas", "Células"),
    ("estetica", "estética"), ("estetico", "estético"),
    ("Estetica", "Estética"),
    ("dermatologicamente", "dermatologicamente"),
    ("opticos", "óticos"),
    ("medula", "medula"),
    ("inovador", "inovador"),
    ("aspeto", "aspeto"),
    ("aparencia", "aparência"),
    ("recipiente", "recipiente"),
    ("fisicas", "físicas"), ("fisicos", "físicos"),
    ("Fisicos", "Físicos"),
    ("quimicos", "químicos"),
    ("nanoesferas", "nanoesferas"),
    ("mesosferas", "mesosferas"),
    ("formula", "fórmula"), ("Formula", "Fórmula"),
    ("formulas", "fórmulas"),
    ("antioxidantes", "antioxidantes"),
    ("ate as", "até às"),
    ("ate o", "até ao"),
    ("dia a dia", "dia-a-dia"),
    ("rosto", "rosto"),
    ("dia de", "dia de"),
    ("manha", "manhã"),
    ("Manha", "Manhã"),
    ("manhas", "manhãs"),
    ("noite", "noite"),
    ("decote", "decote"),
    ("pescoco", "pescoço"),
    ("Pescoco", "Pescoço"),
    ("excecional", "excecional"),
    ("excelencia", "excelência"),
    ("eficacia", "eficácia"),
    ("avancada", "avançada"),
    ("Centro de Ciencia", "Centro de Ciência"),
    ("Centro de Pesquisa", "Centro de Pesquisa"),
    ("Centro de Pesquisa e Ciencia", "Centro de Pesquisa e Ciência"),
    ("PuriOlea", "PuriOlea"),
    ("Lipo-Sphere", "Lipo-Sphere"),
    ("FGF1", "FGF1"),
    ("DERMATOLOGICAMENTE", "DERMATOLOGICAMENTE"),
    ("Ferulico", "Ferúlico"),
    ("Glicolico", "Glicólico"),
    ("Piruvico", "Pirúvico"),
    ("Mandelico", "Mandélico"),
    ("Fitico", "Fítico"),
    ("Salicilico", "Salicílico"),
    ("Acetinado", "Acetinado"),
    ("Acetinico", "Acetínico"),
    ("Lactobionico", "Lactobiónico"),
    ("Galactarico", "Galactárico"),
    ("Glicerretinico", "Glicerretínico"),
    ("Mediterraneo", "Mediterrâneo"),
    ("Mediterranica", "Mediterrânica"),
    ("Aurantium", "Aurantium"),
    ("Hidrocomplexo", "Hidrocomplexo"),
    ("Probiotix", "Probiotix"),
    ("Probiotico", "Probiótico"), ("probiotico", "probiótico"),
    ("Probioticos", "Probióticos"), ("probioticos", "probióticos"),
    ("imunoprotetoras", "imunoprotetoras"),
    ("musica", "música"),
    ("magica", "mágica"),
    ("estagio", "estágio"),
    ("oposto", "oposto"),
    ("excessivos", "excessivos"),
    ("substancias", "substâncias"), ("substancia", "substância"),
    ("Substancia", "Substância"),
    ("dose adequada", "dose adequada"),
    ("dose otima", "dose ótima"),
    ("otima", "ótima"), ("otimo", "ótimo"),
    ("eficaz", "eficaz"),
    ("nucleo", "núcleo"),
    ("sintese", "síntese"),
    ("genetica", "genética"),
    ("biologica", "biológica"), ("biologico", "biológico"),
    ("biologicamente", "biologicamente"),
    ("Numero", "Número"), ("numero", "número"),
    ("Numeros", "Números"),
    ("Tonalidade", "Tonalidade"),
    ("Tonico", "Tónico"), ("tonico", "tónico"),
    ("tonicos", "tónicos"),
    ("Vita", "Vita"),
    ("ASCORBILO", "ASCORBILO"),
    ("ascorbilo", "ascorbilo"),
    ("Polonia", "Polónia"),
    ("opaca", "opaca"),
    ("opaco", "opaco"),
    ("baca", "baça"),
    ("baco", "baço"),
    ("ate 24 horas", "até 24 horas"),
    ("ate 24h", "até 24 h"),
    ("ate o creme", "até ao creme"),
    ("ferulica", "ferúlica"),
    ("Idealine", "Idealine"),
    ("Tiotaina", "Tiotaína"), ("tiotaina", "tiotaína"),
    ("Tioprolina", "Tioprolina"),
    ("Hesperidina", "Hesperidina"),
    ("Ergotioneina", "Ergotioneína"),
    ("Niacinamida", "Niacinamida"),
    ("Pycnogenol", "Pycnogenol"),
    ("Arbutina", "Arbutina"),
    ("Glutationa", "Glutationa"),
    ("Azeloglicina", "Azeloglicina"),
    ("Cyto-Stim", "Cyto-Stim"),
    ("Bakuchiol", "Bakuchiol"),
    ("Chrysinimide", "Chrysinimide"),
    ("Arginina", "Arginina"),
    ("Diosmina", "Diosmina"),
    ("Ceramida", "Ceramida"), ("ceramida", "ceramida"),
    ("ceramidas", "ceramidas"),
    ("Tetrapeptideo", "Tetrapéptido"),
    ("Hexapeptideo", "Hexapéptido"),
    ("Sintese", "Síntese"),
    ("Brilho", "Brilho"),
    ("Sebo", "Sebo"),
    ("DNA", "DNA"),
    ("PGA", "PGA"),
    ("PCL-Lift-Up", "PCL-Lift-Up"),
    ("PCL", "PCL"),
    ("Promatrix", "Promatrix"),
    ("MultiPeptide", "MultiPeptide"),
    ("PuriOlea", "PuriOlea"),
    ("Esticar a pele", "esticar a pele"),
    ("Algumas gotas", "Algumas gotas"),
    ("Para resultados", "Para resultados"),
    ("Soft Focus Powder", "Soft Focus Powder"),
    ("Velvet Focus Powder", "Velvet Focus Powder"),
    ("Bright Focus", "Bright Focus"),
    ("Cellular", "Cellular"),
    ("Imperata", "Imperata"),
    ("Cylindrica", "Cylindrica"),
    ("Cogongrass", "Cogongrass"),
    ("Fuse-Formula", "Fuse-Formula"),
    ("Vita-hexapeptide", "Vita-hexapéptido"),
    ("Vita-hexapeptido", "Vita-hexapéptido"),
    ("SKINFILL-UP", "SKINFILL-UP"),
    ("Triple C-Booster", "Triple C-Booster"),
    ("Forming Complex", "Forming Complex"),
    ("Protect Lash Complex", "Protect Lash Complex"),
    ("Complexo Shellac", "Complexo Shellac"),
    ("Aqua Calcis", "Aqua Calcis"),
    ("ja experimentou", "já experimentou"),
    ("Reactivador", "Reativador"),
    ("reactivando", "reativando"),
    ("Ceratonia Siliqua", "Ceratonia Siliqua"),
    ("Oryza Sativa", "Oryza Sativa"),
    ("Olea Europaea", "Olea Europaea"),
    ("Cannabis Sativa", "Cannabis Sativa"),
    ("Simmondsia chinensis", "Simmondsia chinensis"),
    ("Laminaria Ochroleuca", "Laminaria Ochroleuca"),
    ("Nelumbo Nucifera", "Nelumbo Nucifera"),
    ("Nymphaea alba", "Nymphaea alba"),
    ("Bambusa vulgaris", "Bambusa vulgaris"),
    ("Citrus Aurantium Dulcis", "Citrus Aurantium Dulcis"),
    ("Carmel", "Carmel"),
    ("Honey", "Honey"),
    ("Natural", "Natural"),
    ("Golden", "Golden"),
    ("EUFORBIA", "EUFORBIA"),
    ("Euforbia", "Euforbia"),
    ("Candelila", "Candelila"),
    ("Candelilla", "Candelilla"),
    ("Eskalo", "Eskalo"),
    ("Makula", "Makula"),
    ("Levante", "Levante"),
    # Palavras genericas sem acento
    ("agua", "água"), ("Agua", "Água"),
    ("aguas", "águas"),
    ("humida", "húmida"), ("humido", "húmido"),
    ("Humida", "Húmida"),
    ("diario", "diário"), ("diaria", "diária"),
    ("Diario", "Diário"),
    ("rapida", "rápida"), ("rapido", "rápido"),
    ("rapidamente", "rapidamente"),
    ("textura", "textura"),
    ("intensiva", "intensiva"), ("intensivo", "intensivo"),
    ("eficaz", "eficaz"),
    ("expressao", "expressão"),
    ("geracao", "geração"),
    ("producao", "produção"),
    ("Producao", "Produção"),
    ("reducao", "redução"),
    ("Reducao", "Redução"),
    ("seleccionados", "selecionados"),
    ("selecionados", "selecionados"),
    ("tres ", "três "),
    ("Tres ", "Três "),
    ("inumeras", "inúmeras"),
    ("Reforcado", "Reforçado"),
    ("reforcado", "reforçado"),
    ("Reforca", "Reforça"),
    ("reforca", "reforça"),
    ("reforco", "reforço"),
    ("eficacia", "eficácia"),
    ("avancado", "avançado"),
    ("medio", "médio"), ("media", "média"),
    ("medias", "médias"), ("medios", "médios"),
    ("epiderme", "epiderme"),
    ("camadas", "camadas"),
    ("conferindo", "conferindo"),
    ("polipeptidico", "polipeptídico"),
    ("tripeptidica", "tripeptídica"),
    ("Multinivel", "Multinível"),
    ("multinivel", "multinível"),
    ("niveis", "níveis"),
    ("nivel", "nível"),
    ("Nivel", "Nível"),
    ("Higienizacao", "Higienização"),
    ("higienizacao", "higienização"),
    ("ate ao", "até ao"),
    ("comparativamente", "comparativamente"),
    ("organizacao", "organização"),
    ("Organizacao", "Organização"),
    ("revelacao", "revelação"),
    ("imunoprotectoras", "imunoprotetoras"),
    ("imunoprotectivas", "imunoprotetivas"),
    ("aposta", "aposta"),
    ("Aspeto", "Aspeto"),
    ("excecao", "exceção"),
    ("estabilizada", "estabilizada"),
    ("Sebo", "Sebo"),
    ("inibe", "inibe"),
    ("estimula", "estimula"),
    ("inhibition", "inhibition"),
    ("vinte", "vinte"),
    ("uma vez", "uma vez"),
    ("Indicado", "Indicado"),
    ("preparacao", "preparação"),
    ("contem", "contém"),
    ("Contem", "Contém"),
    ("mantem", "mantém"),
    ("Mantem", "Mantém"),
    ("inovacao", "inovação"),
    ("Inovacao", "Inovação"),
    ("excecional", "excecional"),
    ("excecionalmente", "excecionalmente"),
    ("autorais", "autorais"),
    ("polimero", "polímero"),
    ("multiplos", "múltiplos"),
    ("multipla", "múltipla"),
    ("multiplas", "múltiplas"),
    ("incluido", "incluído"), ("incluida", "incluída"),
    ("Incluido", "Incluído"),
    ("hibrido", "híbrido"), ("hibrida", "híbrida"),
    ("Hibrido", "Híbrido"),
    ("possivel", "possível"),
    ("Possivel", "Possível"),
    ("disponivel", "disponível"),
    ("Disponivel", "Disponível"),
    ("disponiveis", "disponíveis"),
    ("agradavel", "agradável"),
    ("essencial", "essencial"),
    ("essenciais", "essenciais"),
    ("util", "útil"),
    ("rapida ", "rápida "),
    ("indicado", "indicado"),
    ("celular", "celular"),
    ("intensidade", "intensidade"),
    ("intensivamente", "intensivamente"),
    ("hidratante", "hidratante"),
    ("antioxidante", "antioxidante"),
    ("desintoxicante", "desintoxicante"),
    ("Cobertura", "Cobertura"),
    ("regular", "regular"),
    ("revitalizante", "revitalizante"),
    ("estimulante", "estimulante"),
    ("recipiente", "recipiente"),
    ("Centro", "Centro"),
    ("Centro de", "Centro de"),
    ("transepidermico", "transepidérmico"),
    ("transepidermica", "transepidérmica"),
    ("tonico", "tónico"),
    ("Tonico", "Tónico"),
    ("tonificante", "tonificante"),
    ("Tonificante", "Tonificante"),
    ("Garante", "Garante"),
    ("garante", "garante"),
    ("Excelencia", "Excelência"),
    ("Eficacia", "Eficácia"),
    ("nova geracao", "nova geração"),
    ("Recomendado", "Recomendado"),
    ("Adequado", "Adequado"),
    ("adequado", "adequado"),
    ("adequada", "adequada"),
    ("adequadas", "adequadas"),
    ("Indicada", "Indicada"),
    ("indicada", "indicada"),
    ("indicadas", "indicadas"),
    ("indicados", "indicados"),
    ("ate o", "até ao"),
    ("Ate ", "Até "),
    ("apos", "após"),
    ("Apos", "Após"),
    ("simples", "simples"),
    ("Funcional", "Funcional"),
    ("Multifuncional", "Multifuncional"),
    ("Sistema", "Sistema"),
    ("Equilibrio", "Equilíbrio"),
    ("equilibrio", "equilíbrio"),
    ("Beneficios-chave", "Benefícios-chave"),
    ("Beneficios", "Benefícios"),
    ("beneficios", "benefícios"),
    ("colagenio", "colagénio"),
    ("Colagenio", "Colagénio"),
    ("apropriado", "apropriado"),
    ("cosmetico", "cosmético"),
    ("cosmeticos", "cosméticos"),
    ("cosmecêutica", "cosmecêutica"),
    ("Cosmecêutica", "Cosmecêutica"),
    ("dermatologica", "dermatológica"),
    ("dermatologicas", "dermatológicas"),
    ("dermatologico", "dermatológico"),
    ("dermocosmetica", "dermocosmética"),
    ("Dermocosmetica", "Dermocosmética"),
    ("estetica", "estética"),
    ("Estetica", "Estética"),
    ("estatico", "estático"),
    ("medico-estetico", "médico-estético"),
    ("Medico-estetico", "Médico-estético"),
    ("dermatologos", "dermatólogos"),
    ("Dermatologos", "Dermatólogos"),
    ("Aplicar", "Aplicar"),
    ("efeito", "efeito"),
    ("Periodicas", "Periódicas"),
    ("periodicas", "periódicas"),
    ("periodico", "periódico"),
    ("aposta", "aposta"),
    ("cabe", "cabe"),
    ("Polonia", "Polónia"),
    ("polipeptidos", "polipéptidos"),
    ("metabolica", "metabólica"),
    ("Energia", "Energia"),
    ("energia", "energia"),
    ("metabolicas", "metabólicas"),
    ("mitocondrias", "mitocôndrias"),
    ("Mitocondrias", "Mitocôndrias"),
    ("descricao", "descrição"),
    ("Descricao", "Descrição"),
    ("anti-aging", "anti-aging"),
    ("Anti-aging", "Anti-aging"),
    ("vitamina", "vitamina"),
    ("Vitamina", "Vitamina"),
    ("vitaminas", "vitaminas"),
    ("Vitaminas", "Vitaminas"),
    ("FNM", "FNM"),
    ("(FNM)", "(FNM)"),
    ("FPS", "FPS"),
    ("UV", "UV"),
    ("UVA", "UVA"),
    ("UVB", "UVB"),
    ("UVA/UVB", "UVA/UVB"),
    ("HA", "HA"),
    ("SPF", "SPF"),
    ("ETR", "ETR"),
    ("PHA", "PHA"),
    ("NMF", "NMF"),
    ("AGEs", "AGEs"),
    ("PGA", "PGA"),
    ("DNA", "DNA"),
    ("DAY TO NIGHT", "DAY TO NIGHT"),
    ("FLAWLESS SKIN", "FLAWLESS SKIN"),
    ("URBAN GLOW", "URBAN GLOW"),
    ("SKIN VELVET", "SKIN VELVET"),
    ("EXFO", "EXFO"),
    ("VITA", "VITA"),
    ("MESO X", "MESO X"),
    ("P.O.W.E.R.", "P.O.W.E.R."),
    ("S.O.S.", "S.O.S."),
    ("P.O.S.T.", "P.O.S.T."),
    ("E.Y.E.", "E.Y.E."),
    ("N.E.C.K.", "N.E.C.K."),
    ("A.G.E.", "A.G.E."),
    ("C.R.", "C.R."),
    ("M.E.L.A.", "M.E.L.A."),
    ("A.C.", "A.C."),
    ("C.C.", "C.C."),
    ("E.X.F.O.", "E.X.F.O."),
    ("D.E.R.M.A.B.R.A.S.I.O.N.", "D.E.R.M.A.B.R.A.S.I.O.N."),
    # casos finais
    ("ultima", "última"), ("Ultima", "Última"),
    ("ultimas", "últimas"),
    ("ultimo", "último"), ("ultimos", "últimos"),
    ("multiplo", "múltiplo"),
    ("publica", "pública"), ("publico", "público"),
    ("Publica", "Pública"),
    ("praticidade", "praticidade"),
    ("pratico", "prático"), ("pratica", "prática"),
    ("Pratico", "Prático"),
    ("autonomia", "autonomia"),
    ("autonoma", "autónoma"), ("autonomo", "autónomo"),
    ("ambito", "âmbito"),
    ("biomimetico", "biomimético"), ("biomimeticos", "biomiméticos"),
    ("biomimetica", "biomimética"),
    ("BIOMIMETICO", "BIOMIMÉTICO"),
    ("anti-rugas", "anti-rugas"),
    ("Anti-rugas", "Anti-rugas"),
    ("anti-poluicao", "anti-poluição"),
    ("Anti-poluicao", "Anti-poluição"),
    ("poluicao", "poluição"),
    ("Poluicao", "Poluição"),
    ("regenerativa", "regenerativa"),
    ("Regenerativa", "Regenerativa"),
    ("biostimulador", "biostimulador"),
    ("policaprolactona", "policaprolactona"),
    ("Policaprolactona", "Policaprolactona"),
    ("Moringa", "Moringa"),
    ("Vitellaria", "Vitellaria"),
    ("Edelweiss", "Edelweiss"),
    ("edelweiss", "edelweiss"),
    ("Bambu", "Bambu"),
    ("Lotus", "Lótus"),
    ("Nenufar", "Nenúfar"),
    ("lotus", "lótus"),
    ("nenufar", "nenúfar"),
    ("Lecitina", "Lecitina"),
    ("Argao", "Argão"),
    ("argao", "argão"),
    ("macadamia", "macadâmia"),
    ("Macadamia", "Macadâmia"),
    ("Gergelim", "Gergelim"),
    ("gergelim", "gergelim"),
    ("Jojoba", "Jojoba"),
    ("jojoba", "jojoba"),
    ("AGE", "AGE"),
    ("E.F.A.", "E.F.A."),
    ("EFA", "EFA"), ("EFAs", "EFAs"),
    ("(ETR)", "(ETR)"),
    ("Lentilha", "Lentilha"),
    ("lentilha", "lentilha"),
    ("inviolavel", "inviolável"),
    ("estavel", "estável"),
    ("desenvolvido", "desenvolvido"),
    ("Desenvolvido", "Desenvolvido"),
    ("formulado", "formulado"),
    ("Formulado", "Formulado"),
    ("padrao", "padrão"),
    ("Padrao", "Padrão"),
    ("desempenho", "desempenho"),
    ("Aplicar", "Aplicar"),
    ("ja ", "já "),
    (" ja", " já"),
    ("Ja ", "Já "),
    ("usual", "usual"),
    ("habitual", "habitual"),
    ("recomendado", "recomendado"),
    ("Mais", "Mais"),
    ("excelente", "excelente"),
    ("matiz", "matiz"),
    ("nutrir", "nutrir"),
    ("Nutricao", "Nutrição"),
    ("nutricao", "nutrição"),
    ("Bonus", "Bónus"), ("bonus", "bónus"),
    ("Premium", "Premium"),
    ("estimulacao", "estimulação"),
    ("Estimulacao", "Estimulação"),
    ("inibicao", "inibição"),
    ("oxidante", "oxidante"),
    ("Combina", "Combina"),
    ("combina", "combina"),
    ("estudo", "estudo"),
    ("estudos", "estudos"),
    ("Anti-envelhecimento", "Anti-envelhecimento"),
    ("anti-envelhecimento", "anti-envelhecimento"),
    ("anti-idade", "anti-idade"),
    ("Anti-idade", "Anti-idade"),
    ("Antioxidante", "Antioxidante"),
    ("envelhecimento", "envelhecimento"),
    ("Envelhecimento", "Envelhecimento"),
    ("envelhecimento prematuro", "envelhecimento prematuro"),
    ("Hidratacao", "Hidratação"),
    ("Hidratante", "Hidratante"),
    ("Suprema", "Suprema"),
    ("luminoso", "luminoso"),
    ("luminosos", "luminosos"),
    ("Luminoso", "Luminoso"),
    ("acabamento", "acabamento"),
    ("Acabamento", "Acabamento"),
    ("Magia", "Magia"),
    ("delicadas", "delicadas"),
    ("delicado", "delicado"),
    ("delicadamente", "delicadamente"),
    ("Delicada", "Delicada"),
    ("opcao", "opção"),
    ("Opcao", "Opção"),
    ("excessao", "exceção"),
    ("acneica", "acneica"),
    ("Acneica", "Acneica"),
    ("variavel", "variável"),
    ("paragrafos", "parágrafos"),
    ("paragrafo", "parágrafo"),
    ("Maquilhagem", "Maquilhagem"),
    ("maquilhagem", "maquilhagem"),
    ("rosto", "rosto"),
    ("Rosto", "Rosto"),
    ("Aplica", "Aplica"),
    ("brilho", "brilho"),
    ("Brilho", "Brilho"),
    ("brilhante", "brilhante"),
    ("Estimula", "Estimula"),
    ("Reduz", "Reduz"),
    ("reduz", "reduz"),
    ("Acalma", "Acalma"),
    ("acalma", "acalma"),
    ("Hidrata", "Hidrata"),
    ("Combate", "Combate"),
    ("trata", "trata"),
    ("garantia", "garantia"),
    ("Garantia", "Garantia"),
    ("acidos", "ácidos"),
    ("acida", "ácida"),
    ("oleos", "óleos"),
    ("oleo", "óleo"),
    ("amendoa", "amêndoa"),
    ("Amendoa", "Amêndoa"),
    ("amendoas", "amêndoas"),
    ("Cera de Candelila", "Cera de Candelila"),
    ("Candelila", "Candelila"),
    ("Pantenol", "Pantenol"),
    ("pantenol", "pantenol"),
    ("D-pantenol", "D-pantenol"),
    ("multinivel", "multinível"),
    ("Multinivel", "Multinível"),
    ("oxidativo", "oxidativo"),
    ("Oxidativo", "Oxidativo"),
    ("inibidora", "inibidora"),
    ("ondulacao", "ondulação"),
    ("Ondulacao", "Ondulação"),
    ("Calibragem", "Calibragem"),
    ("intensos", "intensos"),
    ("intensa", "intensa"),
    ("intenso", "intenso"),
    ("Olhares", "Olhares"),
    ("olhar", "olhar"),
    ("Olhar", "Olhar"),
    ("Crystal", "Crystal"),
    ("dia/noite", "dia/noite"),
    ("dia ou noite", "dia ou noite"),
    ("ate completa", "até completa"),
    ("decimo", "décimo"),
    ("decima", "décima"),
    ("Recovery", "Recovery"),
    ("Booster", "Booster"),
    ("Tonic", "Tonic"),
    ("Cleanse", "Cleanse"),
    ("Resurfacing", "Resurfacing"),
    ("resurfacing", "resurfacing"),
    ("Mask", "Mask"),
    ("Cream", "Cream"),
    ("Foundation", "Foundation"),
    ("Lip Gloss", "Lip Gloss"),
    ("Wedding Pink", "Wedding Pink"),
    ("Honey Nude", "Honey Nude"),
    ("Dusty Peach", "Dusty Peach"),
    ("Cool Pink", "Cool Pink"),
    ("Give'em Sparkle", "Give'em Sparkle"),
    ("Juicy Coral", "Juicy Coral"),
    ("Sweet Fuchsia", "Sweet Fuchsia"),
    ("Seductive Red", "Seductive Red"),
    ("Oh Carmine", "Oh Carmine"),
    ("Firm Plum", "Firm Plum"),
    ("Cella Maris", "Cella Maris"),
    ("Maris", "Maris"),
    ("BB Cream", "BB Cream"),
    ("CC Cream", "CC Cream"),
    ("Bambu", "Bambu"),
    ("Mascara", "Máscara"),
    ("mascara", "máscara"),
    ("Coffret", "Coffret"),
    ("coffret", "coffret"),
    ("(in vivo)", "(in vivo)"),
    ("in vivo", "in vivo"),
    ("in-vivo", "in-vivo"),
    ("comprovado", "comprovado"),
    ("comprovada", "comprovada"),
    ("clinicos", "clínicos"),
    ("Clinicos", "Clínicos"),
    ("clinico", "clínico"),
    ("clinica", "clínica"),
    ("Clinica", "Clínica"),
    ("clinicas", "clínicas"),
    ("dermatologicamente", "dermatologicamente"),
    ("Testado", "Testado"),
    ("testado", "testado"),
    ("Testada", "Testada"),
    ("testada", "testada"),
    # numeros
    ("100% das utilizadoras", "100% das utilizadoras"),
    ("90% das utilizadoras", "90% das utilizadoras"),
    ("60-30s", "60 s"),
    # mais ações simples
    ("ate ao creme", "até ao creme"),
    ("Cuidado", "Cuidado"),
    ("cuidado", "cuidado"),
    ("Tarifa", "Tarifa"),
    ("PATENTE", "PATENTE"),
    ("Patente", "Patente"),
    ("patenteado", "patenteado"),
    ("Patenteado", "Patenteado"),
    ("patenteados", "patenteados"),
    ("Patenteados", "Patenteados"),
    # Mais ajustes finais
    ("impecavel", "impecável"), ("Impecavel", "Impecável"),
    ("otima", "ótima"), ("Otima", "Ótima"),
    ("otimo", "ótimo"), ("Otimo", "Ótimo"),
    ("otimos", "ótimos"),
    ("extraordinario", "extraordinário"),
    ("Extraordinario", "Extraordinário"),
    ("extraordinaria", "extraordinária"),
    ("realcando", "realçando"),
    ("Realcando", "Realçando"),
    ("realcam", "realçam"),
    ("realca", "realça"),
    ("realce", "realce"),
    ("visivelmente", "visivelmente"),
    ("visivel", "visível"), ("Visivel", "Visível"),
    ("visiveis", "visíveis"),
    ("ultra-elastica", "ultra-elástica"),
    ("ultra-elastico", "ultra-elástico"),
    ("elastica", "elástica"), ("elastico", "elástico"),
    ("Elastica", "Elástica"),
    ("facil", "fácil"), ("Facil", "Fácil"),
    ("faceis", "fáceis"),
    ("Edificavel", "Edificável"),
    ("edificavel", "edificável"),
    ("radiancia", "radiância"),
    ("Radiancia", "Radiância"),
    ("radiante", "radiante"),
    ("Radiante", "Radiante"),
    ("logico", "lógico"), ("logica", "lógica"),
    ("imagem", "imagem"),
    ("Imagem", "Imagem"),
    ("ate ", "até "),
    ("Ate ", "Até "),
    ("alem ", "além "),
    ("Alem ", "Além "),
    ("calida", "cálida"),
    ("Diagnostico", "Diagnóstico"),
    ("diagnostico", "diagnóstico"),
    ("Caracteristicas", "Características"),
    ("caracteristicas", "características"),
    ("hipertensao", "hipertensão"),
    ("Cetilia", "Cetilia"),
    ("medio-escuras", "médio-escuras"),
    ("medias-escuras", "médias-escuras"),
    ("claras-medias", "claras-médias"),
    ("medias", "médias"),
    ("medio", "médio"),
    ("Decote", "Decote"),
    ("simbiose", "simbiose"),
    ("ciclico", "cíclico"),
    ("citadinas", "citadinas"),
    ("repousada", "repousada"),
    ("Indicada", "Indicada"),
    ("envolvendo", "envolvendo"),
    ("intermitente", "intermitente"),
    ("estatica", "estática"),
    ("indica", "indica"),
    ("estatica", "estática"),
    ("estaticos", "estáticos"),
    ("dinamicos", "dinâmicos"),
    ("uniformiza", "uniformiza"),
    ("ascendentes", "ascendentes"),
    ("descendentes", "descendentes"),
    ("perda", "perda"),
    ("perdas", "perdas"),
    ("perda transepidermica", "perda transepidérmica"),
    ("transepidermica", "transepidérmica"),
    ("delicada", "delicada"),
    ("intercelular", "intercelular"),
    ("hidrolipidica", "hidrolipídica"),
    ("Hidrolipidica", "Hidrolipídica"),
    ("hidrolipidico", "hidrolipídico"),
    ("policlinica", "policlínica"),
    ("oncologica", "oncológica"),
    ("Aplicar", "Aplicar"),
    ("Hidratacao", "Hidratação"),
    ("hidratacao", "hidratação"),
    ("hidratado", "hidratado"),
    ("hidratada", "hidratada"),
    ("Hidratado", "Hidratado"),
    ("epico", "épico"),
    ("Epico", "Épico"),
    ("estatico-epico", "estático-épico"),
    ("ja sao", "já são"),
    ("sao ", "são "),
    ("nao ", "não "),
    ("Nao ", "Não "),
    ("luxo", "luxo"),
    ("Luxo", "Luxo"),
    ("Cetilia", "Cetilia"),
    ("PT-PT", "PT-PT"),
    ("estabil", "estábil"),
    ("alergia", "alergia"),
    ("alergias", "alergias"),
    ("Alergias", "Alergias"),
    ("Alergia", "Alergia"),
    ("dose generosa", "dose generosa"),
    ("acomoda", "acomoda"),
    ("PROVA", "PROVA"),
    ("estabilizada", "estabilizada"),
    ("trofas", "trofas"),
    ("Conservar", "Conservar"),
    ("compor", "compor"),
    ("incorporar", "incorporar"),
    ("incorporado", "incorporado"),
    ("Incorporado", "Incorporado"),
    ("dispenser", "dispenser"),
    ("dispenso", "dispenso"),
    ("Aplicar quantidade", "Aplicar quantidade"),
    ("dispensar", "dispensar"),
    ("medidas", "medidas"),
    ("hidrocomplexo", "hidrocomplexo"),
    ("Hidrocomplexo", "Hidrocomplexo"),
    ("propriedade", "propriedade"),
    ("Propriedades", "Propriedades"),
    ("propriedades", "propriedades"),
    ("Disponivel", "Disponível"),
    ("Especifica", "Específica"),
    ("Especifico", "Específico"),
    ("especifica", "específica"),
    ("especifico", "específico"),
    ("especificamente", "especificamente"),
    ("Especificamente", "Especificamente"),
    ("instantaneo", "instantâneo"),
    ("Instantaneo", "Instantâneo"),
    ("instantanea", "instantânea"),
    ("Instantanea", "Instantânea"),
    ("instantaneamente", "instantaneamente"),
    ("Instantaneamente", "Instantaneamente"),
    ("hexapeptide", "hexapéptide"),
    ("hexapeptido", "hexapéptido"),
    ("estavel", "estável"),
    ("matur", "matur"),
    ("inviavel", "inviável"),
    ("polar", "polar"),
    ("organic", "organic"),
    ("organica", "orgânica"),
    ("Organica", "Orgânica"),
    ("organico", "orgânico"),
    ("Organico", "Orgânico"),
    ("Aqua Idealine", "Aqua Idealine"),
    ("Capill Age", "Capill Age"),
    ("Capill Pro", "Capill Pro"),
    ("Eris", "Eris"),
    ("inumeraveis", "inumeráveis"),
    ("biofotonico", "biofotónico"),
    ("Biofotonico", "Biofotónico"),
    ("emolientes", "emolientes"),
    ("Emolientes", "Emolientes"),
    ("Estavel", "Estável"),
    ("excecionalmente", "excecionalmente"),
    ("Sintese", "Síntese"),
    ("conservante", "conservante"),
    ("conservar", "conservar"),
    ("anuncio", "anúncio"),
    ("Aliando", "Aliando"),
    ("agressao", "agressão"),
    ("Agressao", "Agressão"),
    ("agressores", "agressores"),
    ("Agressores", "Agressores"),
    ("pos-tratamento", "pós-tratamento"),
    ("Pos-tratamento", "Pós-tratamento"),
    ("pos-resurfacing", "pós-resurfacing"),
    ("Pos-resurfacing", "Pós-resurfacing"),
    ("ressurfacing", "ressurfacing"),
    ("Ressurfacing", "Ressurfacing"),
    ("pre-tratamento", "pré-tratamento"),
    ("pos ", "pós "),
    ("Pos ", "Pós "),
    ("pos-inflamatoria", "pós-inflamatória"),
    ("pos-inflamatorio", "pós-inflamatório"),
    ("auto-cuidado", "auto-cuidado"),
    ("anti-acne", "anti-acne"),
    ("anti-Inflamatoria", "anti-inflamatória"),
    ("anti-inflamatoria", "anti-inflamatória"),
    ("Anti-Inflamatoria", "Anti-inflamatória"),
    ("anti-inflamatorias", "anti-inflamatórias"),
    ("inflamatoria", "inflamatória"),
    ("inflamatorio", "inflamatório"),
    ("estrategicas", "estratégicas"),
    ("estrategica", "estratégica"),
    ("estrategicos", "estratégicos"),
    ("estrategico", "estratégico"),
    ("logradouro", "logradouro"),
    ("clinicagem", "clinicagem"),
    ("Profissional", "Profissional"),
    ("profissional", "profissional"),
    ("antianvelhecimento", "antienvelhecimento"),
]
# Aplicar substituicoes — usa boundaries para evitar matches dentro de palavras maiores
_FIX_PATS = [(re.compile(r"\b" + re.escape(k) + r"\b"), v) for k, v in FIX_MAP if k != v]

# Regras genericas: terminacoes -cao -> -ção, -coes -> -ções (preservando capitalizacao)
# Exclusoes (palavras corretas terminadas em cao/coes que NAO devem ser alteradas)
_CAO_EXCLUDE = {"trancao","cao","coes"}  # cao isolado pra evitar match em "cao" sozinho como mascara

def _cao_repl(m):
    w = m.group(0)
    if w.lower() in _CAO_EXCLUDE:
        return w
    if w.endswith("coes"):
        return w[:-4] + ("ções" if w[0].islower() else "ções")
    if w.endswith("cao"):
        return w[:-3] + "ção"
    if w.endswith("Coes"):
        return w[:-4] + "Ções"
    if w.endswith("Cao"):
        return w[:-3] + "Ção"
    return w

_CAO_PAT = re.compile(r"\b[A-Za-zÀ-ÿ]+(?:cao|coes)\b")

# -ao final (mao, irmao, algodao, leao) — restrito a finais especificos
_AO_SAFE_MAP = {
    "algodao": "algodão", "Algodao": "Algodão",
    "leao": "leão", "Leao": "Leão",
    "irmao": "irmão", "irmaos": "irmãos",
    "mao": "mão", "maos": "mãos",
    "verao": "verão", "Verao": "Verão",
    "limao": "limão",
    "Sao ": "São ", "sao ": "são ",
    "Instantaneo": "Instantâneo", "instantaneo": "instantâneo",
    "Espontaneo": "Espontâneo",
    "presenca": "presença", "Presenca": "Presença",
    "comeca": "começa", "Comeca": "Começa",
    "fitormonios": "fitormónios",  # PT-PT
    "fitormonio": "fitormónio",
    "Fitormonios": "Fitormónios",
    "Fitormonio": "Fitormónio",
    "hormonios": "hormónios",
    "hormonio": "hormónio",
    "particula": "partícula", "particulas": "partículas",
    "molecula": "molécula", "moleculas": "moléculas",
    "calmante": "calmante",
    "Calmante": "Calmante",
    "calmantes": "calmantes",
    "ultima": "última",
    "Ultima": "Última",
    "ultimas": "últimas",
    "ultimo": "último", "ultimos": "últimos",
    "umidade": "humidade",
    "Humidade": "Humidade",
    # ate/alem removidos daqui — gerenciados via _FIX_PATS com \b boundaries
}
_AO_SAFE_PATS = [(re.compile(r"\b" + re.escape(k) + r"\b"), v) for k, v in _AO_SAFE_MAP.items() if k.endswith(" ") is False] + [
    (re.compile(re.escape(k)), v) for k, v in _AO_SAFE_MAP.items() if k.endswith(" ")
]

def apply_pt(text: str) -> str:
    out = text
    for pat, repl in _FIX_PATS:
        out = pat.sub(repl, out)
    # Aplicar regra generica -cao/-coes -> -ção/-ções
    out = _CAO_PAT.sub(_cao_repl, out)
    # Aplicar pares -ao seguros
    for pat, repl in _AO_SAFE_PATS:
        out = pat.sub(repl, out)
    return out

# Helper para extrair stock numerico
def stock_badge(stock_str: str) -> str:
    s = stock_str.lower()
    if "esgotado" in s or "out of stock" in s:
        return '<span class="badge badge-out">Esgotado</span>'
    m = re.search(r"(\d+)\s*unidade", s)
    if m:
        n = int(m.group(1))
        if n == 1:
            return '<span class="badge badge-low">Última unidade</span>'
        if n <= 3:
            return '<span class="badge badge-low">Stock baixo</span>'
    return ""

def parse_product(block: str) -> dict:
    """Parse um bloco ### N. Nome ate proximo ---."""
    lines = block.strip().splitlines()
    # Primeiro nao-vazio
    title_line = next((l for l in lines if l.startswith("### ")), "")
    # remover "### N." prefixo
    title = re.sub(r"^###\s*\d+\.\s*", "", title_line).strip()

    body = "\n".join(lines)

    def grab(label: str) -> str:
        # captura entre **Label:** e | ou fim de linha
        m = re.search(rf"\*\*{label}:\*\*\s*([^|*\n][^|\n]*?)(?=\s*\||\s*\n|$)", body)
        return m.group(1).strip() if m else ""

    preco = grab("Preco")
    stock = grab("Stock")
    capacidade = grab("Capacidade")
    categoria = grab("Categoria")
    tom = grab("Tom")
    ref = grab("REF")

    # Headline
    m = re.search(r"\*\*Headline:\*\*\s*(.+?)(?:\n\n|\n\*\*)", body, re.S)
    headline = m.group(1).strip() if m else ""

    # Descricao (varios paragrafos ate proximo bloco **X:**  ou  **Resultados clinicos**)
    m = re.search(r"\*\*Descricao:\*\*\s*\n(.+?)(?=\n\*\*[A-ZÀ-ÿ][^*\n]{0,40}?[:\*]\*\*)", body, re.S)
    desc = m.group(1).strip() if m else ""
    # Cortar tudo a partir de "**Resultados" caso tenha vazado
    desc = re.split(r"\n\s*\*\*Resultados", desc)[0].strip()
    desc = re.split(r"\n\s*\*\*Beneficios", desc)[0].strip()
    desc = re.split(r"\n\s*\*\*Como aplicar", desc)[0].strip()
    desc = re.split(r"\n\s*\*\*Ingredientes", desc)[0].strip()
    desc = re.split(r"\n\s*\*\*Precau", desc)[0].strip()
    desc = re.split(r"\n\s*\*\*Status", desc)[0].strip()
    desc = re.split(r"\n\s*\*\*Oferta", desc)[0].strip()
    desc = re.split(r"\n\s*\*\*Nota", desc)[0].strip()
    # split paragrafos por linhas em branco
    desc_paragraphs = [p.strip() for p in re.split(r"\n\s*\n", desc) if p.strip()]

    # Beneficios (lista)
    m = re.search(r"\*\*Beneficios-chave:\*\*\s*\n((?:- .+\n?)+)", body)
    beneficios = []
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if line.startswith("- "):
                beneficios.append(line[2:].strip())

    # Resultados clinicos
    m = re.search(r"\*\*Resultados cl[ií]nicos\*\*[^:\n]*:?\s*\n((?:- .+\n?)+)", body)
    resultados = []
    resultados_label = ""
    if m:
        # tentar capturar label completo (ex: "(estudos in vivo ...)")
        m2 = re.search(r"\*\*Resultados cl[ií]nicos\*\*\s*([^:\n]*):?\s*\n((?:- .+\n?)+)", body)
        if m2:
            resultados_label = m2.group(1).strip()
            for line in m2.group(2).splitlines():
                line = line.strip()
                if line.startswith("- "):
                    resultados.append(line[2:].strip())

    # Como aplicar
    m = re.search(r"\*\*Como aplicar:\*\*\s*(.+?)(?=\n\*\*|\n---|$)", body, re.S)
    como = m.group(1).strip() if m else ""

    # Ingredientes ativos
    m = re.search(r"\*\*Ingredientes ativos[^:]*:\*\*\s*(.+?)(?=\n\*\*|\n---|$)", body, re.S)
    ingredientes = m.group(1).strip() if m else ""

    # Precaucao
    m = re.search(r"\*\*Precau[cç][aã]o:\*\*\s*(.+?)(?=\n\*\*|\n---|$)", body, re.S)
    precaucao = m.group(1).strip() if m else ""

    # Status (Skin Velvet N5)
    m = re.search(r"\*\*Status:\*\*\s*(.+?)(?=\n\*\*|\n---|$)", body, re.S)
    status = m.group(1).strip() if m else ""

    # Oferta especial (K-Wish)
    m = re.search(r"\*\*Oferta especial:\*\*\s*(.+?)(?=\n\*\*|\n---|$)", body, re.S)
    oferta = m.group(1).strip() if m else ""

    return {
        "title": title,
        "preco": preco, "stock": stock, "capacidade": capacidade,
        "categoria": categoria, "tom": tom, "ref": ref,
        "headline": headline,
        "desc_paragraphs": desc_paragraphs,
        "beneficios": beneficios,
        "resultados": resultados,
        "resultados_label": resultados_label,
        "como": como,
        "ingredientes": ingredientes,
        "precaucao": precaucao,
        "status": status,
        "oferta": oferta,
    }

# Parse: dividir em blocos por "### N." considerando secao
sections = {}  # nome_secao -> [produtos]
current = None
section_buf = []
prod_buf = []

# Identificar headings de secao "## DR IRENA ERIS — ROSTO"
section_pattern = re.compile(r"^##\s+(.+)$", re.M)
prod_pattern = re.compile(r"^###\s+(\d+)\.\s+(.+)$", re.M)

# split por "---"
chunks = raw.split("\n---\n")
# Encontrar secao atual percorrendo
sections_order = ["IRENA_ROSTO", "IRENA_MAQ", "KARAJA", "PHFORMULA", "TEN"]
sections_data = {k: [] for k in sections_order}

current_section = None
for chunk in chunks:
    chunk_strip = chunk.strip()
    # Detect section header
    sec_m = re.search(r"^##\s+(.+)$", chunk_strip, re.M)
    if sec_m:
        sec_title = sec_m.group(1).upper()
        if "ROSTO" in sec_title and "IRENA" in sec_title:
            current_section = "IRENA_ROSTO"
        elif "MAQUILHAGEM" in sec_title and "IRENA" in sec_title:
            current_section = "IRENA_MAQ"
        elif "KARAJA" in sec_title:
            current_section = "KARAJA"
        elif "PHFORMULA" in sec_title:
            current_section = "PHFORMULA"
        elif "TEN" in sec_title:
            current_section = "TEN"

    # Detect product
    prod_m = re.search(r"^###\s+(\d+)\.\s+(.+)$", chunk_strip, re.M)
    if prod_m and current_section:
        p = parse_product(chunk_strip)
        # Skip "Reservado" placeholder (### 35 sem dados)
        if not p["preco"] and not p["headline"] and "Reservado" in p["title"]:
            p["placeholder"] = True
        else:
            p["placeholder"] = False
        sections_data[current_section].append(p)

# Reportar contagens
print(f"IRENA ROSTO: {len(sections_data['IRENA_ROSTO'])}")
print(f"IRENA MAQ:   {len(sections_data['IRENA_MAQ'])}")
print(f"KARAJA:      {len(sections_data['KARAJA'])}")
print(f"PHFORMULA:   {len(sections_data['PHFORMULA'])}")
print(f"TEN:         {len(sections_data['TEN'])}")

# Agrupar variantes — produtos com mesmo nome-base (Foundation, Lip Gloss, Photo Finish etc)
# Estrategia: identificar por radical antes do tom/numero

VARIANT_GROUPS = {
    "IRENA_MAQ": [
        ("Day to Night Longwear Foundation", "Day to Night Longwear Foundation SPF 30"),
        ("Flawless Skin Anti-Aging Foundation", "Flawless Skin Anti-Aging Foundation SPF 30"),
        ("Urban Glow Luminous Anti-Pollution Foundation", "Urban Glow Luminous Anti-Pollution Foundation SPF 30"),
        ("Ultimate Shine Lip Gloss", "Ultimate Shine Lip Gloss"),
    ],
    "KARAJA": [
        ("Lapis Corretivo Karaja", "Lápis Corretivo Karaja"),
        ("Photo Finish", "Photo Finish"),
        ("Skin Velvet", "Skin Velvet"),
    ],
    "IRENA_ROSTO": [],
    "PHFORMULA": [],
    "TEN": [],
}

def html_escape(s: str) -> str:
    s = apply_pt(s)
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("Nº", "Nº"))

def render_product_details(p: dict) -> str:
    """Render conteudo expandido de UM produto dentro de <details>."""
    parts = []
    if p["desc_paragraphs"]:
        parts.append("<div class=\"prod-desc\">")
        for para in p["desc_paragraphs"]:
            parts.append(f"  <p>{md_to_html(para)}</p>")
        parts.append("</div>")

    if p["beneficios"]:
        parts.append('<div class="prod-block"><h5>Benefícios-chave</h5><ul class="prod-benefits">')
        for b in p["beneficios"]:
            parts.append(f"  <li>{md_to_html(b)}</li>")
        parts.append("</ul></div>")

    if p["resultados"]:
        label = f' <span class="prod-clinical-label">{md_to_html(p["resultados_label"])}</span>' if p["resultados_label"] else ""
        parts.append(f'<div class="prod-block prod-clinical"><h5>Resultados clínicos{label}</h5><ul>')
        for r in p["resultados"]:
            parts.append(f"  <li>{md_to_html(r)}</li>")
        parts.append("</ul></div>")

    if p["como"]:
        parts.append(f'<div class="prod-block"><h5>Como aplicar</h5><p>{md_to_html(p["como"])}</p></div>')

    if p["ingredientes"]:
        parts.append(f'<div class="prod-block"><h5>Ingredientes ativos</h5><p class="prod-ingredients">{md_to_html(p["ingredientes"])}</p></div>')

    if p["precaucao"]:
        parts.append(f'<div class="prod-block prod-warning"><h5>Precaução</h5><p>{md_to_html(p["precaucao"])}</p></div>')

    if p["oferta"]:
        parts.append(f'<div class="prod-block prod-offer"><h5>Oferta especial</h5><p>{md_to_html(p["oferta"])}</p></div>')

    if p["status"]:
        parts.append(f'<div class="prod-block"><h5>Estado</h5><p>{md_to_html(p["status"])}</p></div>')

    return "\n".join(parts)

def slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:60]

def render_meta_line(p: dict) -> str:
    """Linha de meta: preco · capacidade/tom · categoria."""
    bits = []
    if p["preco"]:
        # extrair so o valor
        pr = p["preco"]
        bits.append(f'<span class="price-tag">{html_escape(pr)}</span>')
    extra = []
    if p["capacidade"]:
        extra.append(html_escape(p["capacidade"]))
    if p["tom"]:
        extra.append(f"Tom: {html_escape(p['tom'])}")
    if p["categoria"]:
        extra.append(html_escape(p["categoria"]))
    if p["ref"]:
        extra.append(f'REF: {html_escape(p["ref"])}')
    meta = " · ".join(extra)
    if meta:
        return f'<p class="price-line">{bits[0] if bits else ""}{" · " if bits and meta else ""}{meta}</p>'
    elif bits:
        return f'<p class="price-line">{bits[0]}</p>'
    return ""

def render_single_card(p: dict, anchor: str) -> str:
    """Card individual com <details> expansor."""
    if p.get("placeholder"):
        return f'''<article class="product product-fisico product-placeholder" id="{anchor}">
  <h3>{html_escape(p["title"])}</h3>
  <p>Espaço reservado para nova entrada conforme atualização do inventário.</p>
</article>'''

    badge = stock_badge(p["stock"])
    badge_html = f' {badge}' if badge else ""
    headline = md_to_html(html_escape(p["headline"])) if p["headline"] else ""

    # Promo badge se preco menciona promocao
    promo = ""
    if "promo" in p["preco"].lower() or "promo" in p["stock"].lower():
        promo = ' <span class="badge badge-promo">Promo</span>'

    meta_line = render_meta_line(p)

    # Primeiro paragrafo de teaser (curto)
    teaser = ""
    if p["desc_paragraphs"]:
        teaser_text = p["desc_paragraphs"][0]
        # cortar em ~180 chars no primeiro ponto final apos 120
        if len(teaser_text) > 180:
            cut = teaser_text.find(". ", 120)
            if cut > 0 and cut < 280:
                teaser_text = teaser_text[:cut + 1]
        teaser = f'<p class="prod-teaser">{md_to_html(teaser_text)}</p>'

    details_content = render_product_details(p)
    has_details = bool(details_content.strip())

    out = [f'<article class="product product-fisico" id="{anchor}">']
    out.append(f'  <h3>{html_escape(p["title"])}{badge_html}{promo}</h3>')
    if headline:
        out.append(f'  <p class="prod-headline">{headline}</p>')
    if meta_line:
        out.append(f'  {meta_line}')
    if teaser:
        out.append(f'  {teaser}')
    if has_details:
        out.append('  <details class="prod-details">')
        out.append('    <summary><span class="prod-details-label">Ver detalhes completos</span></summary>')
        out.append('    <div class="prod-details-body">')
        out.append(details_content)
        out.append('    </div>')
        out.append('  </details>')
    out.append('</article>')
    return "\n".join(out)

def render_variant_family(family_title: str, variants: list, anchor_prefix: str) -> str:
    """Familia de variantes em grid com detalhes do produto-pai expansivel."""
    if not variants:
        return ""
    # Pegar dados comuns do primeiro
    base = variants[0]
    # Descricao comum: primeiros 2 paragrafos do primeiro (sem o trecho de tom)
    common_desc = ""
    if base["desc_paragraphs"]:
        # filtrar paragrafo que comeca falando "Tom"
        keep = []
        for para in base["desc_paragraphs"]:
            keep.append(para)
            if len(keep) >= 2:
                break
        # Remover o trecho final "Tom X" do paragrafo se houver
        common_desc = "\n\n".join(keep)
        common_desc = re.sub(r"\*\*Tom [^*]+?\*\*\s*[^.]*\.\s*$", "", common_desc).strip()

    common_benefits = base["beneficios"]
    common_como = base["como"]
    common_ing = base["ingredientes"]
    common_clinical = base["resultados"]
    common_clinical_label = base["resultados_label"]

    parts = [f'<div class="variant-family" id="{anchor_prefix}-family">']
    parts.append(f'  <h4 class="variant-family-title">{html_escape(family_title)} — {len(variants)} {"tom" if len(variants)==1 else "tons"}</h4>')
    if base["headline"]:
        parts.append(f'  <p class="variant-family-headline">{md_to_html(base["headline"])}</p>')
    # Pegar primeiro paragrafo curto como teaser
    if base["desc_paragraphs"]:
        teaser = base["desc_paragraphs"][0]
        if len(teaser) > 200:
            cut = teaser.find(". ", 140)
            if cut > 0:
                teaser = teaser[:cut+1]
        parts.append(f'  <p class="variant-family-desc">{md_to_html(teaser)}</p>')

    # Grid de variantes
    parts.append('  <div class="variant-grid">')
    for v in variants:
        v_anchor = f"{anchor_prefix}-{slugify(v['tom'] or v['title'])}"
        badge = stock_badge(v["stock"])
        meta_bits = []
        if v["tom"]:
            meta_bits.append(html_escape(v["tom"]))
        if v["capacidade"]:
            meta_bits.append(html_escape(v["capacidade"]))
        meta = " · ".join(meta_bits)
        # Preco
        price = html_escape(v["preco"]) if v["preco"] else "[a confirmar]"
        # Promo gloss N03
        is_promo = "promo" in v["preco"].lower() or "promo" in v.get("stock","").lower()

        parts.append(f'    <div class="variant-card" id="{v_anchor}">')
        parts.append(f'      <h4>{html_escape(v["title"].split(" — ")[-1] if " — " in v["title"] else v["tom"] or v["title"])} {badge}</h4>')
        if meta:
            parts.append(f'      <p class="variant-meta">{meta}</p>')
        parts.append(f'      <p><span class="price-tag">{price}</span></p>')
        if v["stock"]:
            parts.append(f'      <p class="variant-desc">{html_escape(v["stock"])}</p>')
        parts.append('    </div>')
    parts.append('  </div>')

    # Detalhes expansivel — descricao tecnica completa (uma vez para a familia)
    common_block_html = ""
    if common_desc:
        common_block_html += '<div class="prod-desc">'
        for para in re.split(r"\n\s*\n", common_desc):
            if para.strip():
                common_block_html += f"<p>{md_to_html(para.strip())}</p>"
        common_block_html += '</div>'
    if common_benefits:
        common_block_html += '<div class="prod-block"><h5>Benefícios-chave</h5><ul class="prod-benefits">'
        for b in common_benefits:
            common_block_html += f"<li>{md_to_html(b)}</li>"
        common_block_html += '</ul></div>'
    if common_clinical:
        label = f' <span class="prod-clinical-label">{md_to_html(common_clinical_label)}</span>' if common_clinical_label else ""
        common_block_html += f'<div class="prod-block prod-clinical"><h5>Resultados clínicos{label}</h5><ul>'
        for r in common_clinical:
            common_block_html += f"<li>{md_to_html(r)}</li>"
        common_block_html += '</ul></div>'
    if common_como:
        common_block_html += f'<div class="prod-block"><h5>Como aplicar</h5><p>{md_to_html(common_como)}</p></div>'
    if common_ing:
        common_block_html += f'<div class="prod-block"><h5>Ingredientes ativos</h5><p class="prod-ingredients">{md_to_html(common_ing)}</p></div>'

    if common_block_html:
        parts.append('  <details class="prod-details prod-details-family">')
        parts.append('    <summary><span class="prod-details-label">Ver descrição técnica completa</span></summary>')
        parts.append(f'    <div class="prod-details-body">{common_block_html}</div>')
        parts.append('  </details>')

    parts.append('</div>')
    return "\n".join(parts)

# Identificar variantes por titulo
def split_singles_and_families(prods: list, family_keys: list) -> tuple:
    families = {key: [] for key, _ in family_keys}
    singles = []
    for p in prods:
        if p.get("placeholder"):
            singles.append(p)
            continue
        matched = None
        for key, _ in family_keys:
            if key.lower() in p["title"].lower():
                matched = key
                break
        if matched:
            families[matched].append(p)
        else:
            singles.append(p)
    return singles, families

# Sequencia de renderizacao por secao mantendo ordem
def render_section(section_key: str, section_title_html: str, section_intro: str, anchor_id: str) -> str:
    prods = sections_data[section_key]
    family_keys = VARIANT_GROUPS.get(section_key, [])
    family_dict = {key: [] for key, _ in family_keys}
    # mapear ordem
    ordered = []  # lista de ("single", prod) ou ("family", key)
    seen_families = set()
    for p in prods:
        matched = None
        for key, _ in family_keys:
            if key.lower() in p["title"].lower():
                matched = key
                break
        if matched:
            family_dict[matched].append(p)
            if matched not in seen_families:
                ordered.append(("family", matched))
                seen_families.add(matched)
        else:
            ordered.append(("single", p))

    count = len(prods)
    parts = []
    parts.append(f'<h3 id="{anchor_id}" class="subcategoria">{section_title_html} <span class="cat-count">({count})</span></h3>')
    parts.append(f'<p>{section_intro}</p>')

    for kind, val in ordered:
        if kind == "single":
            anchor = f"{anchor_id}-{slugify(val['title'])}"
            parts.append(render_single_card(val, anchor))
        else:
            display_name = next((disp for k, disp in family_keys if k == val), val)
            parts.append(render_variant_family(display_name, family_dict[val], f"{anchor_id}-{slugify(val)}"))

    parts.append(f'<p class="note"><a href="#produtos-fisicos">Voltar ao menu de marcas</a></p>')
    return "\n\n".join(parts)

# Construir bloco completo
new_block = []
new_block.append('<h2 id="produtos-fisicos">Produtos Físicos — Cosmética Profissional</h2>')
new_block.append('<p>A ciência da nossa cabine, agora no seu lavatório. Cosmética profissional selecionada por Sónia Sá: 65 referências individuais entre rosto, maquilhagem e tratamento avançado.</p>')
new_block.append('<p class="note"><strong>Aviso:</strong> As <a href="#condicoes">Condições gerais de serviços</a> (marcação por email, cancelamento 48 h, validade 6 meses) <strong>não se aplicam</strong> aos produtos físicos. Estes seguem a política padrão de venda e devolução de retalho.</p>')
new_block.append('')
new_block.append('<nav class="brand-nav" aria-label="Marcas de produtos físicos">')
new_block.append('  <a href="#prod-irena-rosto">Dr Irena Eris — Rosto</a>')
new_block.append('  <a href="#prod-irena-maq">Dr Irena Eris — Maquilhagem</a>')
new_block.append('  <a href="#prod-karaja">Karaja</a>')
new_block.append('  <a href="#prod-phformula">pHformula</a>')
new_block.append('  <a href="#prod-tenscience">TEN Science</a>')
new_block.append('</nav>')
new_block.append('')

new_block.append(render_section(
    "IRENA_ROSTO",
    "Dr Irena Eris — Rosto",
    "Dermocosmética avançada polaca. Cuidado de rosto de alta tecnologia desenvolvido pelo Centro de Ciência e Pesquisa Dr Irena Eris.",
    "prod-irena-rosto",
))

new_block.append(render_section(
    "IRENA_MAQ",
    "Dr Irena Eris — Maquilhagem",
    "Maquilhagem profissional com cuidado integrado: 22 referências entre bases, rímeis e brilhos labiais.",
    "prod-irena-maq",
))

# Adicionar placeholder #35 Reservado no fim
new_block.append('<article class="product product-fisico product-placeholder" id="prod-irena-maq-reservado">')
new_block.append('  <h3>Reservado — próxima referência Dr Irena Eris</h3>')
new_block.append('  <p>Espaço reservado para nova entrada de maquilhagem Dr Irena Eris, conforme atualização do inventário pela clínica.</p>')
new_block.append('</article>')

new_block.append(render_section(
    "KARAJA",
    "Karaja — Itália",
    "Maquilhagem cosmecêutica italiana. Fórmulas que cuidam enquanto embelezam.",
    "prod-karaja",
))

new_block.append(render_section(
    "PHFORMULA",
    "pHformula — Barcelona",
    "Resurfacing dermatológico médico-estético. Linha profissional para uso doméstico orientado pela especialista.",
    "prod-phformula",
))

# TEN Science placeholder
new_block.append('<h3 id="prod-tenscience" class="subcategoria">TEN Science — Itália <span class="cat-count">(em breve)</span></h3>')
new_block.append('<p>Ciência italiana aplicada ao cuidado integral. Categorias previstas: Corpo, Rosto e Solares.</p>')
new_block.append('<article class="product product-fisico product-placeholder" id="prod-tenscience-placeholder">')
new_block.append('  <h3>Catálogo em breve</h3>')
new_block.append('  <p>A gama TEN Science está em fase de catalogação. Para informações atualizadas sobre disponibilidade e referências, contacte a clínica.</p>')
new_block.append('  <p class="cta-line"><a href="mailto:reservas@aromasdodeserto.pt">Pedir lista de produtos →</a></p>')
new_block.append('</article>')
new_block.append('<p class="note"><a href="#produtos-fisicos">Voltar ao menu de marcas</a> · <a href="#topo">Topo da página</a></p>')

new_html_block = "\n\n".join(new_block) + "\n"

# Carregar loja.html e substituir bloco entre <h2 id="produtos-fisicos"> e a sentinela final
loja = HTML.read_text(encoding="utf-8")

# Localizar o inicio
start_marker = '<h2 id="produtos-fisicos">'
end_marker_text = 'Topo da página</a></p>'

start = loja.find(start_marker)
if start == -1:
    raise SystemExit("ERRO: start marker not found")

# Encontrar o '</p>' que termina com "Topo da pagina"
end = loja.find(end_marker_text, start)
if end == -1:
    raise SystemExit("ERRO: end marker not found")
# avancar ate o fim do </p>
end_close = loja.find("</p>", end)
if end_close == -1:
    raise SystemExit("ERRO: end </p> not found")
end_close += len("</p>")

new_loja = loja[:start] + new_html_block + loja[end_close:]

# Garantir uma quebra de linha apos
HTML.write_text(new_loja, encoding="utf-8")

# Contar cards renderizados
import re as _re
card_count = len(_re.findall(r'class="product product-fisico(?:\s+product-placeholder)?"', new_html_block))
variant_count = len(_re.findall(r'class="variant-card"', new_html_block))
placeholder_count = len(_re.findall(r'class="product product-fisico product-placeholder"', new_html_block))
print(f"\nCards individuais (singles): {card_count - placeholder_count}")
print(f"Placeholders: {placeholder_count}")
print(f"Variant cards (dentro de families): {variant_count}")
print(f"TOTAL SKUs renderizados: {(card_count - placeholder_count) + variant_count}")
print(f"Total de cards visiveis (singles + variant_cards + placeholders): {card_count + variant_count}")
