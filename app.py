# ==============================================================================
# API FAQ — TÉCNICAS DE VENDAS E RAPPORT
# ==============================================================================
# Projeto didático: uma base de conhecimento que qualquer serviço pode consumir
# 
# QUEM PODE USAR ESTA API:
#   - Um chatbot de WhatsApp que responde dúvidas de vendedores
#   - Um site de treinamento que mostra dicas por categoria
#   - Um app mobile de consulta rápida antes de uma reunião
#   - Uma IA que usa as técnicas como contexto para gerar scripts
#   - Uma planilha que importa as perguntas para estudo
#   - Outro sistema de qualquer empresa
#
# Para rodar: python app.py
# ==============================================================================

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_FAQ = os.path.join(PASTA, "faq_vendas.json")

app = Flask(__name__)
CORS(app)

# ==============================================================================
# DADOS INICIAIS — perguntas e respostas sobre técnicas de vendas
# ==============================================================================
# Estes dados são carregados na primeira execução.
# Depois, os alunos podem adicionar mais via POST!

FAQ_INICIAL = [
    {
        "id": 1,
        "categoria": "rapport",
        "pergunta": "O que é rapport?",
        "resposta": "Rapport é a técnica de criar uma conexão genuína com o cliente. Significa 'espelhar' a outra pessoa — usar tom de voz parecido, linguagem corporal similar e demonstrar interesse real pelo que ela diz. Quando há rapport, o cliente sente que você o entende.",
        "exemplo": "Se o cliente fala devagar e em tom calmo, você também fala devagar. Se ele usa termos técnicos, você acompanha. Isso cria confiança.",
        "dica_rapida": "Chame o cliente pelo nome, isso gera conexão imediata.",
        "nivel": "iniciante",
        "tags": ["rapport", "conexão", "espelhamento", "confiança"]
    },
    {
        "id": 2,
        "categoria": "rapport",
        "pergunta": "Como criar rapport nos primeiros 30 segundos?",
        "resposta": "Nos primeiros 30 segundos, o cliente decide se confia em você. Sorria naturalmente, faça contato visual, use o nome da pessoa e encontre algo em comum — pode ser o bairro, o time, o clima, qualquer coisa.",
        "exemplo": "Vendedor: 'Bom dia, João! Vi que você veio do Kobrasol, eu moro pertinho de lá. Como está o trânsito hoje?'",
        "dica_rapida": "Observe algo no ambiente do cliente (foto, troféu, camiseta) e comente.",
        "nivel": "iniciante",
        "tags": ["rapport", "primeira impressão", "conexão", "abertura"]
    },
    {
        "id": 3,
        "categoria": "rapport",
        "pergunta": "O que é espelhamento?",
        "resposta": "Espelhamento é reproduzir sutilmente a linguagem corporal, tom de voz e ritmo de fala do cliente. Não é imitar — é acompanhar naturalmente. O cérebro humano se sente mais confortável com pessoas parecidas.",
        "exemplo": "Se o cliente cruza os braços e fala baixo, você também adota uma postura mais contida. Se ele é expansivo e fala alto, você aumenta a energia.",
        "dica_rapida": "Espelhe com 3-5 segundos de atraso para parecer natural.",
        "nivel": "intermediario",
        "tags": ["rapport", "espelhamento", "linguagem corporal", "PNL"]
    },
    {
        "id": 4,
        "categoria": "escuta_ativa",
        "pergunta": "O que é escuta ativa?",
        "resposta": "Escuta ativa é ouvir com atenção total, sem interromper, e mostrar ao cliente que você entendeu. Envolve repetir palavras-chave, fazer perguntas de aprofundamento e evitar pensar na resposta enquanto o outro fala.",
        "exemplo": "Cliente: 'Preciso de algo que resolva meu problema de organização'. Vendedor: 'Entendi, organização é prioridade pra você. Me conta: o que mais te atrapalha hoje na organização?'",
        "dica_rapida": "Repita a última frase do cliente como pergunta: 'Organização?'. Ele vai se abrir mais.",
        "nivel": "iniciante",
        "tags": ["escuta ativa", "comunicação", "empatia", "perguntas"]
    },
    {
        "id": 5,
        "categoria": "escuta_ativa",
        "pergunta": "Como fazer perguntas abertas?",
        "resposta": "Perguntas abertas começam com 'como', 'o que', 'por que', 'me conta'. Elas fazem o cliente falar mais e revelar necessidades que ele nem sabia que tinha. Evite perguntas que se respondem com sim ou não.",
        "exemplo": "Errado: 'Você precisa de um notebook?' (sim/não). Certo: 'Me conta como você usa o computador no dia a dia?' (abre a conversa).",
        "dica_rapida": "Comece com 'Me ajuda a entender...' — funciona sempre.",
        "nivel": "iniciante",
        "tags": ["perguntas abertas", "escuta ativa", "necessidades", "descoberta"]
    },
    {
        "id": 6,
        "categoria": "gatilhos_mentais",
        "pergunta": "O que são gatilhos mentais?",
        "resposta": "Gatilhos mentais são estímulos que influenciam a decisão de compra de forma inconsciente. Os principais são: escassez (pouco estoque), urgência (promoção acaba hoje), prova social (muita gente comprou), autoridade (especialista recomenda) e reciprocidade (dar algo antes de pedir).",
        "exemplo": "Escassez: 'Esse modelo tem só mais 3 unidades'. Prova social: '200 clientes compraram esse mês'. Urgência: 'Esse preço vale até sexta'.",
        "dica_rapida": "Use no máximo 2 gatilhos por conversa. Mais que isso parece manipulação.",
        "nivel": "intermediario",
        "tags": ["gatilhos mentais", "persuasão", "escassez", "urgência", "prova social"]
    },
    {
        "id": 7,
        "categoria": "gatilhos_mentais",
        "pergunta": "Como usar prova social sem mentir?",
        "resposta": "Prova social funciona melhor quando é verdadeira. Mostre avaliações reais, quantidade de vendas, depoimentos de clientes ou cases de sucesso. O cliente pensa: 'se tanta gente comprou e gostou, deve ser bom'.",
        "exemplo": "'Esse produto tem 4.8 estrelas com 500 avaliações no site. A maioria dos clientes elogia a durabilidade.'",
        "dica_rapida": "Mostre o celular com avaliações reais. Ver é mais forte que ouvir.",
        "nivel": "iniciante",
        "tags": ["prova social", "gatilhos mentais", "avaliações", "confiança"]
    },
    {
        "id": 8,
        "categoria": "objecoes",
        "pergunta": "O que fazer quando o cliente diz 'está caro'?",
        "resposta": "Nunca discuta o preço diretamente. Primeiro, entenda o que 'caro' significa para ele: caro comparado a quê? Caro porque não cabe no orçamento? Ou caro porque não viu valor? Depois, mostre o custo-benefício ou ofereça condições de pagamento.",
        "exemplo": "Cliente: 'Tá caro'. Vendedor: 'Entendo. Me ajuda a entender: caro comparado a outro produto que você viu, ou caro pro seu orçamento atual? Porque se dividir em 12x fica R$49 por mês'.",
        "dica_rapida": "Nunca diga 'mas é barato'. Diga 'entendo, vamos ver como encaixar no seu orçamento'.",
        "nivel": "intermediario",
        "tags": ["objeções", "preço", "negociação", "valor"]
    },
    {
        "id": 9,
        "categoria": "objecoes",
        "pergunta": "E quando o cliente diz 'vou pensar'?",
        "resposta": "'Vou pensar' quase sempre significa que o cliente tem uma objeção que não expressou. Sua missão é descobrir qual é, sem pressionar. Pergunte com genuína curiosidade o que ficou em aberto.",
        "exemplo": "Vendedor: 'Claro, é importante pensar bem. Só pra eu te ajudar melhor: o que exatamente você quer avaliar? O produto em si, o preço ou a forma de pagamento?'",
        "dica_rapida": "Respeite o tempo do cliente. Combine um retorno: 'Posso te ligar quinta pra tirar qualquer dúvida?'",
        "nivel": "intermediario",
        "tags": ["objeções", "vou pensar", "fechamento", "follow-up"]
    },
    {
        "id": 10,
        "categoria": "fechamento",
        "pergunta": "Quando é a hora certa de fechar a venda?",
        "resposta": "Sinais de que o cliente está pronto: ele faz perguntas sobre entrega, garantia ou pagamento; pega o produto na mão; faz contas mentalmente; olha para o acompanhante buscando aprovação. Quando perceber esses sinais, pare de apresentar e comece a fechar.",
        "exemplo": "Cliente: 'E a garantia cobre quanto tempo?'. Isso é sinal de compra! Vendedor: 'Dois anos. Quer que eu já separe pra você?'",
        "dica_rapida": "Não tenha medo de perguntar: 'Vamos fechar?'. O pior que pode acontecer é um 'ainda não'.",
        "nivel": "intermediario",
        "tags": ["fechamento", "sinais de compra", "momento certo", "decisão"]
    },
    {
        "id": 11,
        "categoria": "fechamento",
        "pergunta": "O que é fechamento por alternativa?",
        "resposta": "Em vez de perguntar 'quer comprar?', você oferece duas opções que ambas levam à compra. O cliente sente que está no controle porque está escolhendo, não sendo pressionado.",
        "exemplo": "'Você prefere o modelo preto ou o azul?' / 'Quer pagar no cartão em 6x ou no PIX com desconto?' — ambas pressupõem que ele já decidiu comprar.",
        "dica_rapida": "Ofereça sempre 2 opções, nunca 3+. Muitas opções paralisam.",
        "nivel": "intermediario",
        "tags": ["fechamento", "alternativa", "decisão", "técnica"]
    },
    {
        "id": 12,
        "categoria": "pos_venda",
        "pergunta": "Por que o pós-venda é tão importante?",
        "resposta": "Conquistar um cliente novo custa 5 a 7 vezes mais que manter um existente. O pós-venda transforma um comprador em fã: ele volta, recomenda para amigos e defende a marca. Uma mensagem perguntando se está satisfeito pode gerar 3 vendas futuras.",
        "exemplo": "3 dias após a venda: 'Oi Maria! Tudo bem com o produto? Qualquer dúvida pode me chamar!' — isso surpreende e fideliza.",
        "dica_rapida": "Crie um alarme no celular: 3 dias, 15 dias e 30 dias após cada venda, mande mensagem.",
        "nivel": "iniciante",
        "tags": ["pós-venda", "fidelização", "relacionamento", "recomendação"]
    }
]

# ==============================================================================
# FUNÇÕES DE DADOS
# ==============================================================================

def carregar_faq():
    if os.path.exists(ARQUIVO_FAQ):
        try:
            with open(ARQUIVO_FAQ, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def salvar_faq(dados):
    with open(ARQUIVO_FAQ, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def proximo_id(lista):
    if not lista:
        return 1
    return max(item.get('id', 0) for item in lista) + 1

# ==============================================================================
# ROTAS DA API
# ==============================================================================

# --- PÁGINA INICIAL: documentação da API ---
@app.route('/')
def home():
    return jsonify({
        'api': 'FAQ Técnicas de Vendas e Rapport',
        'versao': '1.0',
        'descricao': 'Base de conhecimento sobre vendas que qualquer serviço pode consumir',
        'endpoints': {
            'GET /api/faq': 'Lista todas as perguntas (filtros: ?categoria=rapport&nivel=iniciante&tag=confiança)',
            'GET /api/faq/<id>': 'Busca uma pergunta por ID',
            'GET /api/faq/buscar?q=texto': 'Busca por palavra-chave na pergunta ou resposta',
            'GET /api/categorias': 'Lista as categorias disponíveis',
            'GET /api/dica-do-dia': 'Retorna uma dica aleatória',
            'POST /api/faq': 'Adiciona nova pergunta (alunos podem contribuir!)',
            'PUT /api/faq/<id>': 'Atualiza uma pergunta existente',
            'DELETE /api/faq/<id>': 'Remove uma pergunta',
            'GET /api/estatisticas': 'Números gerais da base',
            'GET /api/health': 'Status da API',
        },
        'categorias_disponiveis': ['rapport', 'escuta_ativa', 'gatilhos_mentais', 'objecoes', 'fechamento', 'pos_venda'],
        'niveis': ['iniciante', 'intermediario', 'avancado'],
        'total_perguntas': len(carregar_faq())
    })

# --- HEALTH CHECK ---
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# --- LISTAR FAQ (com filtros opcionais) ---
@app.route('/api/faq', methods=['GET'])
def listar_faq():
    faq = carregar_faq()

    # Filtro por categoria: /api/faq?categoria=rapport
    categoria = request.args.get('categoria')
    if categoria:
        faq = [f for f in faq if f.get('categoria', '').lower() == categoria.lower()]

    # Filtro por nível: /api/faq?nivel=iniciante
    nivel = request.args.get('nivel')
    if nivel:
        faq = [f for f in faq if f.get('nivel', '').lower() == nivel.lower()]

    # Filtro por tag: /api/faq?tag=confiança
    tag = request.args.get('tag')
    if tag:
        faq = [f for f in faq if tag.lower() in [t.lower() for t in f.get('tags', [])]]

    return jsonify({
        'sucesso': True,
        'perguntas': faq,
        'total': len(faq),
        'filtros_aplicados': {
            'categoria': categoria,
            'nivel': nivel,
            'tag': tag
        }
    })

# --- BUSCAR POR PALAVRA-CHAVE ---
@app.route('/api/faq/buscar', methods=['GET'])
def buscar_faq():
    q = request.args.get('q', '').lower().strip()

    if not q:
        return jsonify({'sucesso': False, 'mensagem': 'Parâmetro ?q= é obrigatório'}), 400

    faq = carregar_faq()
    resultados = [
        f for f in faq
        if q in f.get('pergunta', '').lower()
        or q in f.get('resposta', '').lower()
        or q in f.get('exemplo', '').lower()
        or q in f.get('dica_rapida', '').lower()
        or q in ' '.join(f.get('tags', [])).lower()
    ]

    return jsonify({
        'sucesso': True,
        'busca': q,
        'resultados': resultados,
        'total': len(resultados)
    })

# --- DICA DO DIA (aleatória) ---
@app.route('/api/dica-do-dia', methods=['GET'])
def dica_do_dia():
    import random
    faq = carregar_faq()
    if not faq:
        return jsonify({'sucesso': False, 'mensagem': 'Nenhuma dica cadastrada'}), 404

    dica = random.choice(faq)
    return jsonify({
        'sucesso': True,
        'dica': {
            'categoria': dica.get('categoria'),
            'pergunta': dica.get('pergunta'),
            'dica_rapida': dica.get('dica_rapida'),
            'exemplo': dica.get('exemplo')
        }
    })

# --- LISTAR CATEGORIAS ---
@app.route('/api/categorias', methods=['GET'])
def listar_categorias():
    faq = carregar_faq()
    categorias = {}
    for f in faq:
        cat = f.get('categoria', 'sem_categoria')
        categorias[cat] = categorias.get(cat, 0) + 1

    return jsonify({
        'sucesso': True,
        'categorias': categorias,
        'total_categorias': len(categorias)
    })

# --- BUSCAR POR ID ---
@app.route('/api/faq/<int:id>', methods=['GET'])
def buscar_por_id(id):
    faq = carregar_faq()
    for f in faq:
        if f.get('id') == id:
            return jsonify({'sucesso': True, 'pergunta': f})
    return jsonify({'sucesso': False, 'mensagem': 'Pergunta não encontrada'}), 404

# --- ADICIONAR PERGUNTA (alunos contribuem!) ---
@app.route('/api/faq', methods=['POST'])
def adicionar_faq():
    try:
        dados = request.json

        if not dados.get('pergunta') or not dados.get('resposta'):
            return jsonify({
                'sucesso': False,
                'mensagem': 'Campos "pergunta" e "resposta" são obrigatórios'
            }), 400

        faq = carregar_faq()

        nova = {
            'id': proximo_id(faq),
            'categoria': dados.get('categoria', 'geral').strip(),
            'pergunta': dados['pergunta'].strip(),
            'resposta': dados['resposta'].strip(),
            'exemplo': dados.get('exemplo', '').strip(),
            'dica_rapida': dados.get('dica_rapida', '').strip(),
            'nivel': dados.get('nivel', 'iniciante'),
            'tags': dados.get('tags', []),
            'autor': dados.get('autor', 'Aluno anônimo'),
            'criado_em': datetime.now().strftime('%d/%m/%Y %H:%M')
        }

        faq.append(nova)
        salvar_faq(faq)

        return jsonify({
            'sucesso': True,
            'mensagem': f"Pergunta adicionada por {nova['autor']}!",
            'pergunta': nova
        }), 201

    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': str(e)}), 500

# --- ATUALIZAR PERGUNTA ---
@app.route('/api/faq/<int:id>', methods=['PUT'])
def atualizar_faq(id):
    try:
        dados = request.json
        faq = carregar_faq()

        for f in faq:
            if f.get('id') == id:
                f['pergunta'] = dados.get('pergunta', f['pergunta'])
                f['resposta'] = dados.get('resposta', f['resposta'])
                f['exemplo'] = dados.get('exemplo', f['exemplo'])
                f['dica_rapida'] = dados.get('dica_rapida', f['dica_rapida'])
                f['categoria'] = dados.get('categoria', f['categoria'])
                f['nivel'] = dados.get('nivel', f['nivel'])
                f['tags'] = dados.get('tags', f['tags'])
                f['atualizado_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                salvar_faq(faq)
                return jsonify({'sucesso': True, 'mensagem': 'Atualizada!', 'pergunta': f})

        return jsonify({'sucesso': False, 'mensagem': 'Não encontrada'}), 404
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': str(e)}), 500

# --- EXCLUIR PERGUNTA ---
@app.route('/api/faq/<int:id>', methods=['DELETE'])
def excluir_faq(id):
    try:
        faq = carregar_faq()
        for i, f in enumerate(faq):
            if f.get('id') == id:
                removida = faq.pop(i)
                salvar_faq(faq)
                return jsonify({'sucesso': True, 'mensagem': 'Removida!', 'pergunta': removida})
        return jsonify({'sucesso': False, 'mensagem': 'Não encontrada'}), 404
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': str(e)}), 500

# --- ESTATÍSTICAS ---
@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    faq = carregar_faq()
    categorias = {}
    niveis = {}
    for f in faq:
        cat = f.get('categoria', 'geral')
        niv = f.get('nivel', 'indefinido')
        categorias[cat] = categorias.get(cat, 0) + 1
        niveis[niv] = niveis.get(niv, 0) + 1

    return jsonify({
        'sucesso': True,
        'total_perguntas': len(faq),
        'por_categoria': categorias,
        'por_nivel': niveis,
        'atualizado_em': datetime.now().isoformat()
    })

# ==============================================================================
# INICIALIZAÇÃO
# ==============================================================================

if __name__ == '__main__':
    # Se não existir o arquivo, cria com as perguntas iniciais
    if not os.path.exists(ARQUIVO_FAQ):
        salvar_faq(FAQ_INICIAL)
        print(f"✅ Base criada com {len(FAQ_INICIAL)} perguntas sobre vendas!")
    else:
        faq = carregar_faq()
        print(f"✅ Base carregada com {len(faq)} perguntas")

    porta = int(os.environ.get('PORT', 5000))

    print(f"\n🚀 API FAQ de Vendas rodando em http://localhost:{porta}")
    print(f"   Categorias: rapport, escuta_ativa, gatilhos_mentais, objecoes, fechamento, pos_venda")
    print(f"   Teste: http://localhost:{porta}/api/faq?categoria=rapport")
    print(f"   Dica do dia: http://localhost:{porta}/api/dica-do-dia")
    print(f"   Buscar: http://localhost:{porta}/api/faq/buscar?q=preço")
    print(f"\n   Pressione CTRL+C para parar\n")

    app.run(debug=False, host='0.0.0.0', port=porta)
