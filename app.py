from flask import Flask, render_template, request, jsonify
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta'

jogos = {}

def estado_inicial():
    return {
        'tabuleiro': [['', '', ''] for _ in range(3)],
        'turno': 'X',
        'vencedor': None,
        'jogadas': 0
    }

def verificar_vencedor(tabuleiro):
    # Verifica linhas, colunas e diagonais
    linhas_colunas = [tabuleiro[i][:] for i in range(3)] + [[tabuleiro[i][j] for i in range(3)] for j in range(3)]
    diagonais = [[tabuleiro[i][i] for i in range(3)], [tabuleiro[i][2-i] for i in range(3)]]
    
    for linha in linhas_colunas + diagonais:
        if len(set(linha)) == 1 and linha[0] != '':
            return linha[0]
    if all(tabuleiro[i][j] != '' for i in range(3) for j in range(3)):
        return 'Empate'
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novo_jogo', methods=['GET'])
def novo_jogo():
    id_jogo = uuid4().hex
    jogos[id_jogo] = estado_inicial()
    return jsonify({'id_jogo': id_jogo})

@app.route('/jogar', methods=['POST'])
def jogar():
    dados = request.json
    id_jogo = dados['id_jogo']
    linha = dados['linha']
    coluna = dados['coluna']
    jogo = jogos.get(id_jogo)

    if not jogo or jogo['tabuleiro'][linha][coluna] or jogo['vencedor']:
        return jsonify({'erro': 'Jogada inválida'}), 400

    # Faz a jogada
    jogo['tabuleiro'][linha][coluna] = jogo['turno']
    jogo['jogadas'] += 1

    # Verifica se há um vencedor
    vencedor = verificar_vencedor(jogo['tabuleiro'])
    if vencedor:
        jogo['vencedor'] = vencedor
    else:
        # Alterna o turno
        jogo['turno'] = 'O' if jogo['turno'] == 'X' else 'X'
    
    return jsonify(jogo)

@app.route('/estado/<id_jogo>', methods=['GET'])
def estado(id_jogo):
    jogo = jogos.get(id_jogo)
    if not jogo:
        return jsonify({'erro': 'Jogo não encontrado'}), 404
    return jsonify(jogo)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
