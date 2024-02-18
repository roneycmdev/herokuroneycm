from flask import Flask, jsonify, request, send_from_directory, abort
import uuid

app = Flask(__name__, static_url_path='', static_folder='static')

games = {}

def new_game_state():
    return {
        'board': [' ' for _ in range(9)],
        'current_player': 'X',
        'winner': None,
        'draw': False,
    }

def check_winner(game):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if game['board'][condition[0]] == game['board'][condition[1]] == game['board'][condition[2]] != ' ':
            game['winner'] = game['current_player']
            return True
    if ' ' not in game['board']:
        game['draw'] = True
        return True
    return False

def switch_player(game):
    game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/game/new', methods=['POST'])
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = new_game_state()
    return jsonify({'game_id': game_id})

@app.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    if game_id not in games:
        abort(404, description="Game not found")
    
    game = games[game_id]
    data = request.get_json()
    position = data.get('position')
    player = data.get('player')

    if player != game['current_player']:
        return jsonify({'error': 'Not your turn'}), 400

    if position is None or game['board'][position] != ' ' or game['winner'] or game['draw']:
        return jsonify({'error': 'Invalid move'}), 400
    
    game['board'][position] = player
    
    if not check_winner(game):
        switch_player(game)

    return jsonify(game)

@app.route('/game/<game_id>/status', methods=['GET'])
def game_status(game_id):
    if game_id not in games:
        abort(404, description="Game not found")
    return jsonify(games[game_id])

@app.route('/game/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    if game_id not in games:
        abort(404, description="Game not found")
    
    games[game_id] = new_game_state()
    return jsonify(games[game_id])

if __name__ == '__main__':
    app.run(debug=True)
