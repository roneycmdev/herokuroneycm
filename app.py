from flask import Flask, jsonify, request, abort
from threading import Lock

app = Flask(__name__)

games = {}
game_id_counter = 1
lock = Lock()

def new_game_state():
    return {
        'board': [' ' for _ in range(9)],
        'players': {'X': None, 'O': None},  # Rastreia os identificadores dos jogadores
        'current_player': 'X',
        'winner': None,
        'draw': False,
    }

def generate_game_id():
    global game_id_counter
    with lock:
        game_id = str(game_id_counter)
        game_id_counter += 1
    return game_id

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != ' ':
            return board[condition[0]]
    if ' ' not in board:
        return 'Draw'
    return None

@app.route('/game/new', methods=['POST'])
def create_game():
    game_id = generate_game_id()
    games[game_id] = new_game_state()
    return jsonify({'game_id': game_id})

@app.route('/game/<game_id>/join', methods=['POST'])
def join_game(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    player_id = request.json.get('player_id')
    if game['players']['X'] is None:
        game['players']['X'] = player_id
        return jsonify({'role': 'X'})
    elif game['players']['O'] is None:
        game['players']['O'] = player_id
        return jsonify({'role': 'O'})
    else:
        abort(400, "Game is full.")

@app.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    
    player_id = request.json.get('player_id')
    position = request.json.get('position')
    
    if game['players'][game['current_player']] != player_id:
        abort(403, "It's not your turn.")
    
    if game['board'][position] != ' ' or game['winner']:
        abort(400, "Invalid move.")
    
    game['board'][position] = game['current_player']
    winner = check_winner(game['board'])
    if winner:
        game['winner'] = winner if winner != 'Draw' else None
        game['draw'] = True if winner == 'Draw' else False
    else:
        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    
    return jsonify(game)

@app.route('/game/<game_id>/status', methods=['GET'])
def game_status(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    return jsonify(game)

if __name__ == "__main__":
    app.run(debug=True)
