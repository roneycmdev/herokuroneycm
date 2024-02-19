from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Estado inicial do jogo
game_state = {
    'board': [' ' for _ in range(9)],
    'current_player': 'X',
    'winner': None,
    'draw': False,
    'players': []
}

def check_winner(board):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] and board[condition[0]] != ' ':
            return board[condition[0]]
    if ' ' not in board:
        return 'Draw'
    return None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_game')
def handle_join_game():
    if len(game_state['players']) < 2:
        game_state['players'].append(request.sid)
        emit('player_joined', {'player': 'X' if len(game_state['players']) == 1 else 'O', 'id': request.sid}, room=request.sid)
        if len(game_state['players']) == 2:
            emit('start_game', game_state, broadcast=True)

@socketio.on('make_move')
def handle_make_move(data):
    index = data['position']
    player = data['player']
    if game_state['board'][index] == ' ' and player == game_state['current_player']:
        game_state['board'][index] = player
        winner = check_winner(game_state['board'])
        if winner:
            game_state['winner'] = winner
            game_state['draw'] = True if winner == 'Draw' else False
        else:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
        emit('update_game', game_state, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
