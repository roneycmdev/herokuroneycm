from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta'

# Estado inicial do jogo
def estado_inicial():
    return {
        'tabuleiro': [['', '', ''], ['', '', ''], ['', '', '']],
        'turno': 'X',
        'vencedor': None,
        'jogadas': 0  # Contador de jogadas para verificar empate
    }

@app.route('/')
def index():
    session['jogo'] = estado_inicial()
    return render_template('index.html')

@app.route('/jogar', methods=['POST'])
def jogar():
    dados = request.get_json()
    linha = dados['linha']
    coluna = dados['coluna']
    jogo = session.get('jogo', estado_inicial())

    # Verifica se a célula já está ocupada
    if jogo['tabuleiro'][linha][coluna] == '':
        jogo['tabuleiro'][linha][coluna] = jogo['turno']
        jogo['jogadas'] += 1
        # Verificar vencedor ou mudar turno
        if verificar_vencedor(jogo['tabuleiro'], jogo['turno']):
            jogo['vencedor'] = jogo['turno']
        elif jogo['jogadas'] == 9:  # Verifica empate
            jogo['vencedor'] = 'Empate'
        else:
            jogo['turno'] = 'O' if jogo['turno'] == 'X' else 'X'
        session['jogo'] = jogo
    return jsonify(jogo)

@app.route('/estado', methods=['GET'])
def estado():
    return jsonify(session.get('jogo', estado_inicial()))

def verificar_vencedor(tabuleiro, turno):
    # Verificar linhas, colunas e diagonais para o vencedor
    for i in range(3):
        if all([c == turno for c in tabuleiro[i]]) or all([tabuleiro[j][i] == turno for j in range(3)]):
            return True
    if tabuleiro[0][0] == turno and tabuleiro[1][1] == turno and tabuleiro[2][2] == turno:
        return True
    if tabuleiro[0][2] == turno and tabuleiro[1][1] == turno and tabuleiro[2][0] == turno:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
