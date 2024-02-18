from flask import Flask, jsonify, request, abort

app = Flask(__name__, static_folder='static')

games = {}
game_id_counter = 1

def new_game_state():
    return {'board': [' ' for _ in range(9)], 'current_player': 'X', 'winner': None, 'draw': False}

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
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    data = request.json
    position = data['position']
    if position < 0 or position > 8 or game['board'][position] != ' ' or game['winner']:
        return jsonify({'error': 'Invalid move'}), 400
    game['board'][position] = game['current_player']
    game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    return jsonify(game)

@app.route('/game/<game_id>/status', methods=['GET'])
def game_status(game_id):
    game = games.get(game_id)
    if not game:
        abort(404, "Game not found.")
    return jsonify(game)

if __name__ == '__main__':
    app.run(debug=True)
