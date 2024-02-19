from flask import Flask, jsonify, request

app = Flask(__name__, static_folder='static')

games = {}
game_id_counter = 1

def new_game_state():
    return {'board': [' ' for _ in range(9)], 'current_player': 'X', 'winner': None}

def check_winner(board):
    win_patterns = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in win_patterns:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/game/new', methods=['POST'])
def create_game():
    global game_id_counter
    game_id = str(game_id_counter)
    games[game_id] = new_game_state()
    game_id_counter += 1
    return jsonify({'game_id': game_id})

@app.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    game = games[game_id]
    data = request.json
    position, player = data['position'], data['player']
    if game['board'][position] != ' ' or game['winner']:
        return jsonify({'error': 'Invalid move'}), 400
    game['board'][position] = player
    winner = check_winner(game['board'])
    if winner:
        game['winner'] = winner
    else:
        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    return jsonify(game)

@app.route('/game/<game_id>', methods=['GET'])
def game_status(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(games[game_id])

if __name__ == '__main__':
    app.run(debug=True)
