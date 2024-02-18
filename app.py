from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Estado inicial do jogo
game_state = {
    'board': [' ' for _ in range(9)],  # Tabuleiro de jogo 3x3 como uma lista
    'current_player': 'X',  # X começa
    'winner': None,
    'draw': False
}

@app.route('/')
def index():
    return render_template_string(open('static/index.html').read())  # Servir o HTML diretamente

@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = data.get('position')
    player = data.get('player')

    if game_state['board'][position] == ' ' and (game_state['winner'] is None and not game_state['draw']):
        game_state['board'][position] = player
        if check_winner():
            game_state['winner'] = player
        elif ' ' not in game_state['board']:
            game_state['draw'] = True
        else:
            switch_player()
        return jsonify(game_state)
    else:
        return jsonify({'error': 'Movimento inválido ou jogo já terminou.'}), 400

@app.route('/status', methods=['GET'])
def game_status():
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset_game():
    game_state['board'] = [' ' for _ in range(9)]
    game_state['current_player'] = 'X'
    game_state['winner'] = None
    game_state['draw'] = False
    return jsonify(game_state)

def check_winner():
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if game_state['board'][condition[0]] == game_state['board'][condition[1]] == game_state['board'][condition[2]] != ' ':
            return True
    return False

def switch_player():
    game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'

if __name__ == '__main__':
    app.run(debug=True)
