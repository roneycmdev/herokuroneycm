from flask import Flask, jsonify, request, send_from_directory, abort
import os

app = Flask(__name__, static_folder='static')

games = {}
game_id_counter = 1

def new_game_state():
    return {
        'board': [' ' for _ in range(9)],
        'players': {'X': None, 'O': None},
        'current_player': 'X',
        'winner': None,
        'draw': False,
    }

def check_winner(board):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/game/new', methods=['POST'])
def create_game():
    global game_id_counter
    game_id = str(game_id_counter)
    games[game_id] = new_game_state()
    game_id_counter += 1
    return jsonify({'game_id': game_id})

@app.route('/game/<game_id>/join', methods=['POST'])
def join_game(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    player_role = request.json.get('role')
    if player_role in game['players'] and game['players'][player_role] is None:
        game['players'][player_role] = request.remote_addr  # Use remote_addr as a simple player identifier
        return jsonify({'role': player_role})
    else:
        abort(400, "Invalid request or role already taken.")

@app.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    if game['winner'] or game['draw']:
        return jsonify(game)  # Game over
    
    player_role = request.json.get('role')
    position = request.json.get('position')
    if game['current_player'] != player_role or game['board'][position] != ' ':
        abort(400, "Invalid move or not your turn.")
    
    game['board'][position] = player_role
    winner = check_winner(game['board'])
    if winner:
        game['winner'] = winner if winner != 'Draw' else None
        game['draw'] = True if winner == 'Draw' else False
    else:
        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    return jsonify(game)

@app.route('/game/<game_id>', methods=['GET'])
def game_status(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    return jsonify(game)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
