from flask import Flask, jsonify, request, send_from_directory, abort
import threading

app = Flask(__name__, static_url_path='', static_folder='static')

games = {}
game_id_counter = 1
lock = threading.Lock()

def new_game_state():
    return {
        'board': [' ' for _ in range(9)],
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

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/game/new', methods=['POST'])
def create_game():
    game_id = generate_game_id()
    games[game_id] = new_game_state()
    return jsonify({'game_id': game_id})

@app.route('/game/<game_id>/status', methods=['GET'])
def game_status(game_id):
    game = games.get(game_id)
    if game is None:
        abort(404, "Game not found.")
    return jsonify(game)

@app.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")

    data = request.json
    player = data['player']
    position = data['position']

    if game['board'][position] != ' ' or game['winner'] or game['draw']:
        return jsonify({'error': 'Invalid move'}), 400
    
    game['board'][position] = player

    # Check for win or draw
    # Implement win check logic here

    game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    return jsonify(game)

if __name__ == "__main__":
    app.run(debug=True)
